import json

def format_lon(x):
    return '{}°W'.format(-x) if (x < 0) else'{}°E'.format(x) 

def format_lat(x):
    return '{}°S'.format(-x) if (x < 0) else'{}°N'.format(x) 

def format_extent(obj):
    if obj['extent'] is None:
        return ''
    lon0, lon1 = [format_lon(x) for x in obj['extent'][:2]]
    lat0, lat1 = [format_lat(x) for x in obj['extent'][2:]]
    return '({}&nbsp;{}) ({}&nbsp;{})'.format(lon0, lat0, lon1, lat1)

def format_center(obj):
    args = obj['args']
    if 'central_latitude' not in args:
        return format_lon(args['central_longitude'])
    return '{} {}'.format(format_lon(args['central_longitude']),
                          format_lat(args['central_latitude']))

def format_thumbnail(proj, obj):
    name = proj.replace('.', '-') + '.png'
    return '![thumbnail of {}](images/{})'.format(proj, name)



def build_doc(obj):
    lines = ['# Projection Info']
    lines.append('Name | Projection | Extent | Thumbnail')
    lines.append('------ | -------- | ------ | ---------')
    for k, v in obj.items():
        v['extent'] = format_extent(v)
        v['center'] = format_center(v)
        name = v['name']
        if 'proj-string' in v:
            name += '<br/><em>{}</em>'.format(v['proj-string'])
        if 'description' in v:
            name += '<br/>{}'.format(v['description'])
        v['thumbnail'] = format_thumbnail(k, v)
        v['proj'] = v.get('proj-string', '')
        lines.append('{} | {} | {extent} | {thumbnail}'.format(
                            k, name, **v))
    return '\n'.join(lines) 






if __name__ == '__main__':
    with open('data/projection_info.json') as f:
        obj = json.load(f)
    md = build_doc(obj)
    with open('doc/projection_info.md', 'w') as f:
        f.write(md)