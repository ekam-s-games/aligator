CHILD_QUERY = """SELECT
    request.hijo,
    request.nombre,
    stat.nombre,
    request.padre,
    typeRequest.nombre,
    businessLine.nombre,
    business.nombre,
    app.nombre,
    devArea.nombre,
    development_factory.nombre,
    user.username
FROM
    tigouneappqadev.estados stat
    JOIN tigouneappqadev.requerimientos request ON stat.id = request.estado_id
    JOIN tigouneappqadev.tiposolicituds typeRequest ON request.tiposolicitud_id = typeRequest.id
    JOIN tigouneappqadev.lineanegocios businessLine ON request.lineanegocio_id = businessLine.id
    JOIN tigouneappqadev.negocios business ON request.negocio_id = business.id
    JOIN tigouneappqadev.aplicacions app ON request.aplicacion_id = app.id
    JOIN tigouneappqadev.area_desarrollos devArea ON request.area_desarrollo_id = devArea.id
    JOIN tigouneappqadev.fabricas development_factory ON request.fabrica_id = development_factory.id
    LEFT JOIN tigouneappqadev.usuarios user ON request.coordinador = user.id
WHERE
    request.hijo = ?"""


INTERESTED_QUERY = """SELECT 
    users.username
FROM
    mantis_tigo_indra.tigo_user_group_table AS groups
        JOIN
    mantis_tigo_indra.tigo_usergroup_user_table AS usergroup ON groups.id = usergroup.id_group
        JOIN
    mantis_tigo_indra.mantis_user_table AS users ON usergroup.id_user = users.id
WHERE
    groups.name IN (?)"""


TESTLINK_QUERY = """SELECT 
    nh.name NOMBRE
FROM
    tigo_testlink.testplans tp
        JOIN
    tigo_testlink.nodes_hierarchy nh ON tp.id = nh.id
WHERE
    nh.name LIKE '?'"""


MANTIS_QUERY = """SELECT name, numberReq
FROM mantis_tigo_indra.mantis_project_table
WHERE numberReq = '?'"""


APPEND_USER_TO_PROJECT = "CALL sbtg0001_p_appendUserToProject('{}', '{}')"
