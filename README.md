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

            ==   => es andaPor
            !=   => no es

            <   => es unCachitoMeno
            <=   => es menorOIgual
            
            >   => es unCachitoMa
            >=   => es mayorOIgual

            +- => es maomeno 

            1 es andaPor 1 => 1
            a es andaPor 1 => 0
            a es andaPor 32 => 1
            a no es b => 0
            a no es 2 => 1

            5 es unCachitoMeno 6 => 1
            5 es unCachitoMeno 4 => 0

            5 es maomeno 4 => 0
            5 es maomeno 4 => 1

        Conditions Combination:
            and => y
            or => o

            1 es andaPor 1 y 2 es andaPor 2 => 1
            1 es andaPor 1 y 2 es andaPor 1 => 0

            1 es andaPor 1 o 2 es andaPor 2 => 1
            1 es andaPor 1 o 2 es andaPor 1 => 1
            1 es andaPor 2 o 2 es andaPor 1 => 0



    CREDITS:
    CodePulse tutorial: https://www.youtube.com/playlist?list=PLZQftyCk7_SdoVexSmwy_tBgs7P0b97yD

    CodePulse tutorial repo: https://github.com/davidcallanan/py-myopl-code
    
    Tutorial based on: https://ruslanspivak.com/lsbasi-part1/

    The code its based on CodePulse Tutorial, with modifications.