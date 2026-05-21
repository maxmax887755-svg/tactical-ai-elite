def detectar_formacion(jugadores):

    if len(jugadores) < 7:
        return "Desconocida"

    ys = sorted([y for x,y in jugadores])

    defensa = 0
    medio = 0
    ataque = 0

    altura = max(ys) - min(ys)

    if altura == 0:
        return "Desconocida"

    for y in ys:

        pos = (y - min(ys)) / altura

        if pos < 0.33:
            defensa += 1

        elif pos < 0.66:
            medio += 1

        else:
            ataque += 1

    return f"{defensa}-{medio}-{ataque}"