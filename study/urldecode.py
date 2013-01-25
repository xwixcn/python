def urldecode( query ):
    '''
    decode the param
    '''
    d = {}
    a = query.split( '&' )
    value = []
    result = []
    for s in a:
        if s.find( '=' ):
            k, v = map( urllib.unquote, s.split( '=' ) )
            value.append( v )
    result = [value[i:i + 2] for i in range( 0, len( value ) - 1, 2 )]
    return result
