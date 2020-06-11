# CheLang
 
Basic usage:
    CONSOLE:
        python shell.py

        Operations:
            + => ma
            - => meno
            * => por
            / => dividido
            ** => ala
            () => ()

            2 ma 2 => 4
            2 por 5 => 20
            2 ala 2 => 4
            1 + 2 * 3 => 9
            1 + (2 * 3) => 7

        Declare variables:

            che (variable_name) es (value. just numbers)

            che messi es 10

        Declare multiple variables:

            che (variable_name) es che (variable_2_name) es ... es (value. just numbers)
            
            che a es che b es che c es 32

        Conditions:
            (1 => true 0 => false)

            ==   => es igual
            !=   => no es

            <   => es menor
            <=   => es menorOIgual
            
            >   => es mayor
            >=   => es mayorOIgual

            1 es igual 1 => 1
            a es igual 1 => 0
            a es igual 32 => 1
            a no es b => 0
            a no es 2 => 1

            5 es menor 6 => 1
            5 es menor 4 => 0

        Conditions Combination:
            and => y
            or => o

            1 es igual 1 y 2 es igual 2 => 1
            1 es igual 1 y 2 es igual 1 => 0

            1 es igual 1 o 2 es igual 2 => 1
            1 es igual 1 o 2 es igual 1 => 1
            1 es igual 2 o 2 es igual 1 => 0