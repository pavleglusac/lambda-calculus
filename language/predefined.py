predefined_expressions = {
    'T': 'λx.λy.x',
    'F': 'λx.λy.y',
    'or': 'λp.λq.((p p) q)',
    'and': 'λp.λq.((p q) p)',
    'not': 'λp.((p λx.λy.y) λa.λb.a)',

}
