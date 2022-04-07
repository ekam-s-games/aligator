import json


# `testing` or `production`
# ENV = 'production'


BUSINESS_LINE = {
    'fijo': 'fijo',
    'movil': 'movil',
    'móvil': 'movil'
}


DEV_FACTORY = {
    'accenture': 'accenture',
    'indra': 'indra',
    'tata': 'tata',
    'tcs': 'tata'
}


DEV_TEAMS = {
    'accenture': 't_laccentu',
    'indra': {
        'movil': 't_lindramo',
        'fijo': 't_lindrafi'
    },
    'tata': 't_ltatacos'
}


QA_TEAMS = {
    'fijo': 't_sophfijo',
    'movil': 't_sopmovil'
}


APP_TEAMS = {
    'bts': 't_bts',
    'crm/siebel': {'t_crmmovil', 't_siebelfi', 't_intmovil'},
    'crm': 't_crmmovil',
    'crm portal': 't_crmmovil',
    'click': 't_gtcclick',
    'gtc': 't_gtcclick',
    'brm': 't_lindramo',
    'sap': 't_mayudasa',
    'mss': 't_mssfijo',
    'osb': 't_osmfijo',
    'osm': 't_osmfijo',
    'recaudos': 't_recaudos',
    'bus movil/siebel': {'t_siebelfi', 't_intmovil'},
    'epos/siebel': {'t_siebelfi', 't_intmovil'},
    'orquestador siebel-open': {'t_siebelfi', 't_intmovil'},
    'siebel': {'t_siebelfi', 't_intmovil'}
}


DEV_AREA = {
    'brm': 't_lindramo',
    'crm': 't_crmmovil',
    'digital': 't_intmovil',
    'siebel fijo': 't_siebelfi'
}


OPTIONS = [
    "B2B",
    "CBS",
    "COPS",
    "CRM",
    "DATA-MIGRATION",
    "DIGITAL",
    "DTH",
    "DWH",
    "FIJO",
    "FINANCIERA",
    "GARANTIAS",
    "HOGARES",
    "HPD",
    "LEGADOS",
    "MIFYL",
    "OPERACIONES",
    "POE",
    "RFC",
    "SIEBEL",
    "TRANSVERSALES"
]


def normalize_str(arg: str) -> str:
    special_chars = [
        ["_", "-", "–", ",", ":", "(", ")", "/", "&", "á", "à", "ä", "ç", "é",
         "è", "ë", "í", "ì", "ï", "ñ", "ó", "ò", "ö", "ú", "ù", "ü"],
        [" ", " ", " ", " ", " ", " ", " ", " ", "y", "a", "a", "a", "c", "e",
         "e", "e", "i", "i", "i", "n", "o", "o", "o", "u", "u", "u"]
    ]
    arg = arg.lower()
    for i in range(len(special_chars[0])):
        if special_chars[0][i] in arg:
            arg = arg.replace(special_chars[0][i], special_chars[1][i])

    while '  ' in arg:
        arg = arg.replace('  ', ' ')

    arg = arg.split(' ')
    for i in range(len(arg)):
        arg[i] = arg[i][0].upper() + arg[i][1:]
    return ''.join(arg)


def is_set(_set: set) -> bool:
    return True if type(_set) is set else False


def is_dict(_dict: dict) -> bool:
    return True if type(_dict) is dict else False


def is_str(arg: str) -> bool:
    return True if type(arg) is str else False


def spliter(character: str, *args: tuple) -> list:
    """
    El método `spliter()` retorna una nueva lista basada en la entregada al parámetro `args`, la cual requerirá
    sub-dividir sus ítems según el carácter pasado al parámetro `character`.
    Intentando separar cada ítem de la lista según el carácter pasado al parámetro `character`; la lista resultante es
    agregada a la lista `result_list` y retornada una vez finalizado el proceso.
    :param character: Corresponde al carácter de separación.
    :param args: Corresponde al listado de ítems de la lista a procesar.
    :return: Retorna una lista luego de separar los ítems
    """
    result_list = []
    if is_str(character) and len(character) == 1 and len(args) > 0:
        for item in args:
            item = str(item).strip()
            result_list += item.split(character) if len(item) else result_list
    return result_list


def extract_numbers(request_name: str) -> list:
    """
    El método `extract_numbers()` retorna una lista de enteros incorporados en el nombre del requerimiento entregado
    por parámetro. Este nombre puede ser compuesto (según lo establecido por el cliente) o separado por underlines o
    espacios.
    :param request_name: Hace referencia a una lista de argumentos de entrada.
    :return: Retorna una lista de números enteros
    """
    basic_number = ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9')
    result_list, number = list(), ''

    for c in request_name:
        if c in basic_number:
            number += c
        else:
            result_list.append(number) if number else None
            number = ''

    return result_list


def prefix(arg):
    __prefix = {
        "Día a día - Desarrollo Menor": "DM",
        "Desarrollo Menor": "DM",
        "Día a día - Fixes": "FIX",
        "Fixes": "FIX",
    }
    return __prefix[arg] if arg in __prefix else 'REQ'


# def dbs() -> dict:
#     n = json.loads(''.join([line for line in open('../.config')]))
#     return n[ENV]['db']
#
#
# def uris() -> dict:
#     n = json.loads(''.join([line for line in open('../.config')]))
#     return n[ENV]['uri']


if __name__ == '__main__':
    a = dbs()
    b = uris()
    print(a['mantis'])
    print(b['mantis'])
