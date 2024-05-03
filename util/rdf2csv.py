import csv
import datetime
import random
from typing import Union, Tuple

from rdflib import Graph, URIRef, IdentifiedNode, BNode
from rdflib.term import Node, Literal


def _get_key(resource: Node) -> str:
    if isinstance(resource, URIRef):
        # e.g. http://www.wikidata.org/entity/Q20546206
        if '#' in resource:
            return resource.rsplit('#', 1)[-1]
        else:
            return resource.rsplit('/', 1)[-1]

    elif isinstance(resource, BNode):
        # import pdb; pdb.set_trace()
        pass
        raise NotImplementedError()
    else:
        # import pdb; pdb.set_trace()
        pass
        raise NotImplementedError()


COLUMN_IDS = {
    # hash of full URI: local part of URI
}


def _get_col_id(property: Node) -> str:
    if isinstance(property, URIRef):
        property_hash = hash(property)
        col_id = COLUMN_IDS.get(property_hash)

        if col_id is None:
            if '#' in property:
                col_id = property.rsplit('#', 1)[-1]
            else:
                col_id = property.rsplit('/', 1)[-1]

            # check if there is already a column ID stored in COLUMN_IDS, but
            # from a different URI namespace, e.g. http://foo.com/name is
            # already known, and now we have http:bar.com/name . In both cases
            # the column ID would be 'name'. However, the values should not
            # end up in the same column as their respective semantics might
            # differ. Thus, we add a number to the newly found 'name' and make
            # it 'name1'
            base_col_id = col_id
            counter = 0
            while col_id in COLUMN_IDS.values():
                counter += 1
                col_id = base_col_id + str(counter)

            COLUMN_IDS[property_hash] = col_id

        return col_id
    else:
        raise Exception('Found property that is not a URI')


def _get_value(value: Node) -> Union[str, None]:
    if isinstance(value, URIRef):
        if '#' in value:
            return value.rsplit('#', 1)[-1]
        else:
            return value.rsplit('/', 1)[-1]

    elif isinstance(value, BNode):
        # import pdb; pdb.set_trace()
        pass
        raise NotImplementedError()

    elif isinstance(value, Literal):
        if not value.language == 'en':
            return None
        # import pdb; pdb.set_trace()
        return str(value)

    else:
        # import pdb; pdb.set_trace()
        pass
        raise Exception(f'Unexpected type {type(value)} of {value}')


def _parse_coordinates(wkt_point_str: str) -> Tuple[float, float]:
    # e.g. 'Point(-95.333333333 41.483333333)'
    val = wkt_point_str.split('(')[-1].split(')')[0]
    lon_str, lat_str = val.split(' ')

    return float(lat_str), float(lon_str)


def _resolve_geom(geom_uri: Node, g: Graph) -> Tuple[float, float]:
    query_results = g.query(
        f'SELECT ?wkt '
        f'WHERE {{ '
        f'  <{str(geom_uri)}> <http://www.opengis.net/ont/geosparql#asWKT> ?wkt '
        f'}}')

    for result in query_results:
        # there should at most be one result

        # get first projection value, i.e., ?wkt
        result_literal = result[0]
        lat, lon = _parse_coordinates(str(result_literal))

    if len(query_results) == 0:
        raise Exception(f'No coordinates found for {geom_uri}')

    return lat, lon


def convert(input_file_path: str, output_file_path: str):
    g = Graph()
    g.parse(input_file_path)

    # nested dict to be converted into csv(s) later
    data = {}
    uris_to_skip = set()
    header = []

    for s, p, o in g:
        # s is assumed to be a URI or blank node
        if s in uris_to_skip:
            continue

        key: str = _get_key(s)

        # p is assumed to be a URI
        # special treatment of geometries
        if p == URIRef('http://www.opengis.net/ont/geosparql#hasGeometry'):
            try:
                lat, lon = _resolve_geom(o, g)
            except Exception as e:
                print(e)
                continue
            uris_to_skip.add(o)

            if data.get(key) is None:
                data[key] = {}

            if 'lat' not in header:
                header.append('lat')
                header.append('lon')

            data[key]['lat'] = lat
            data[key]['lon'] = lon

            continue

        else:
            column_id = _get_col_id(p)
        value = _get_value(o)

        if value is None:
            continue

        if data.get(key) is None:
            data[key] = {}
        if column_id not in header:
            header.append(column_id)
        data[key][column_id] = value

    with open(output_file_path, 'w') as csv_file:
        csv_writer = csv.writer(csv_file)

        header_row = ['id'] + header + ['date']
        csv_writer.writerow(header_row)

        for id_ in data:
            row = [id_]
            for col in header:
                row.append(data[id_].get(col, ''))

            # dummy time stamps
            # row.append(datetime.date.fromtimestamp(
            #     int(random.gauss(1360000000, 400000000))).isoformat())
            csv_writer.writerow(row)
