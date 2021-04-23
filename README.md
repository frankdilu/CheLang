# CheLang &middot; [![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://github.com/frankdilu/CheLang/blob/master/LICENSE) [![Comprame yerba pal mate](https://img.shields.io/badge/Donate-MercadoPago-blueviolet)](https://www.mercadopago.com.ar/checkout/v1/redirect?pref_id=268208624-4f7bbe17-8a6c-4c99-b0c8-86c1016d2a0d) 

CheLang es un lenguaje de programacion esoterico argento. Ni mas, ni menos.
Con la agradable jerga argenta que nos identifica.

## Instalacion

Ver las [releases](https://github.com/frankdilu/CheLang/releases).

Descargas:

Instalador MSI (Con PATH. Es la que va. La casa lo recomienda.)

ZIP Builded

ZIP Source (Requiere python y modulo "playsound")

## Uso

Instalado con MSI:

      `chelang` (en consola (Con el PATH.))

Con la version buildeada o con MSI:

      Doble click en CheLang.exe (Es obvio flaco media pila)

Con el source:

      python cli.py (en consola)

      python cli.py ./nombreDeArchivo.che

## Cosas de Argento

Claramente, como todo buen argento, el programa no compila ni fines de semana ni los feriados.
Esto ultimo claramente si no esta el flag `--milicos`

No se puede declarar una variable "dolar", eso claramente lo maneja el Banco Central.
Se puede revisar el precio del dolar con su funcion "Dolar()". Pero tenes que estar seguro que no es un precio fijo. Habemus inflacion.

Podes llamar a la "Campora()" cuando quieras y vas a notar su presencia tan particular. Tene en cuenta que, cada vez que se los llama, hay inflacion. Por lo que el "Dolar()" se ve afectado.

Claramente somos inclusivos y aceptamos a los que hablan ingles, entonces pidiendo un "HalloEbribodi()" un expresidente (defraudado por una reconocida cantante que no lo esperó) les va a dar la bienvenida con su magnifico nivel de ingles y queriendo tirar unos pasos.

Como somos patrios ante todo, podemos hacerle honor a la Patria diciendo "Argentina()".

Pero, siendo realistas, el pais es un poco inseguro. Por lo que incluimos un tutorial de qué hacer si entra un "Chorro()" en nuestro hogar.

Si estamos cansados, podemos "Boludear(n)" un rato para aclarar la mente y seguir mandandole fruta.

## Syntaxis
```
Esquema del ReadMe:
      Expresion en CheLang => return / expresion regular

      NO HAY CaSe SenSiTiVe keywords. El ReadMe usa CamelCase para mas claridad

# COMENTARIOS CON EL # jashtag

Operaciones:
      ma => +
      meno => -
      por => *
      dividido => / (retorna flotante)
      aLa => **
      moduleame => % (modulo)
      () => ()
      
      "" => "" (strings)
      [a,b,c] => [a,b,c]


ej:
      2.3 ma 2 => 4.3
      .8 ma 2 => 2.8
      .8 meno 2 => -1.2
      2 por 5 => 10
      2 aLa 2 => 4
      1 ma 2 por 3 => 7
      (1 ma 2) por 3 => 9
      10 dividido 2 => 5.0
      5 moduleame 2 => 1
      6 moduleame 2 => 0

      "a" por 10 => "aaaaaaaaaa"

      "marado " ma "marado" => "marado marado"

      [a,b,c] ma d => [a,b,c,d]
      [a,b,c] ma [d,e] => [a,b,c,d,e]
      [a,b] por 3 => [a,b,a,b,a,b]
      [a,b][0] => a 
      (Siendo a, b, c, d y e variables declaradas previamente, vite.)

Declaracion de variables:

      che (nombreDeVariable) es (valor)
      che (nombreDeVariable) seigual (valor)
      che (nombreDeVariable) son (valor)
      
      digamos que (nombreDeVariable) es (valor)
      digamos que (nombreDeVariable) seigual (valor)
      digamos que (nombreDeVariable) son (valor)
      

      che messi es 10
      che messi es "grosso"
      che sueldo seigual 0
      che doYdo son 4

      digamos que sueldo seigual 0
      digamos que doYdo son 4

      messi  => 10
      sueldo => 0

Declaracion de multiples variables:

      che (nombreDeVariable) es che (variable_2_name) es ... es (valor)

      che a es che b es che c es 32

      o

      che (nombreDeVariable), (nombreDeVariable), (nombreDeVariable) es (valor)

      che messi, maradona son 10

Condiciones:
  (1 => true 0 => false)

      anda por      => ==
      no es        => !=
      es nakever   => !==

      es unCachitoMeno =>   <
      es menorOIgual   =>   <=

      es unCachitoMa   =>   >
      es mayorOIgual   =>   >=

      es maomeno => +- (Es como el == pero le pifia un 20%. Ta re copado)

ej:
      1 anda por 1 => 1
      a anda por 1 => 0
      a anda por 32 => 1
      a no es b => 0
      a no es 2 => 1
      a es nakever 2 => 1
      a es nakever b => 0

      5 es unCachitoMeno 6 => 1
      5 es unCachitoMeno 4 => 0

      10 es maomeno 13 => 0
      10 es maomeno 12 => 1
      10 es maomeno 8 => 1
      10 es maomeno 10 => 1

      "abc" anda por 1 => 1
      "" anda por 1 => 0  (si el string tiene uno o mas caracteres le manda true)

Combinacion de variables:
      y => and / &&
      o => or / ||

      1 anda por 1 y 2 anda por 2 => 1
      1 anda por 1 y 2 anda por 1 => 0
      1 anda por 2 y 2 anda por 1 => 0

      1 anda por 1 o 2 anda por 2 => 1
      1 anda por 1 o 2 anda por 1 => 1
      1 anda por 2 o 2 anda por 1 => 0


Los ife y esas cosas:
      ponele que => if
      tonce      => then
      oSi        => elif
      aLoSumo    => else

      ponele que messi no es 10 tonce 0 aLoSumo 1 => 1
      ponele que messi no es 9 tonce 0 aLoSumo 1  => 0

      ponele que a no es messi tonce 0 oSi a anda por a tonce 1 aLoSumo 6 => 0

      ponele que a no es a tonce 0 oSi messi anda por messi tonce 1 aLoSumo 6 => 1

For / While:
      agarra por => for
      hasta => to
      de a  => step
      tonce => then
      mientras => while
      piquete => break
      segui de largo => continue


      che mirtha es 0
      agarra por i es 0 hasta 10 tonce che mirtha es mirtha ma 30 => mirtha = 300

      che mirtha es 0
      agarra por i es 0 hasta 10 de a 2 tonce che mirtha es mirtha ma 30 => mirtha = 150

      mientras 1 es 1 tonce che mirtha es mirtha ma 1 => infinite loop => mirtha forever
      
      che i es 0
      mientras i es unCachitoMa meno 10 tonce che i es i meno 1 => i = -10

Funciones:
      definime => def / function
      (a, b, c) => (a, b, c)
      => =>  () => expr (Solo una expresion. No tiene "hastaaca" final.)
      hastaaca => } (Aceptando mas de una expresion)
      tirame => return

      definime fibonacci(n)=> ponele que n anda por 0 tonce 0 oSi n anda por 1 tonce 1 aLoSumo (fibonacci(n meno 1) ma fibonacci(n meno 2))

      definime fibonacci(n) => 
            ponele que n anda por 0 tonce
                  tirame 0 
            oSi n anda por 1 tonce 
                  tirame 1 
            aLoSumo 
                  tirame (fibonacci(n meno 1) ma fibonacci(n meno 2))
            hastaaca
      
      Cuchame( fibonacci(10) ) (just one expr (the if))

      definime welcome()
            che name es Traeme("Decime tu nombre, dale :")
            Cuchame("Que onda " ma name ma ". Todo bien?")
      hastaaca

      welcome()   (Tiene varias expresiones. Declara la variable y le manda al Cuchame)

Cosas de fabrica:
      Constantes:
            "Milanesa" = "Carne"
            "Macri" = "Gato"
            "AltoGuiso" = 15
            "Vacio" =  Empty (Ojo que no se puede operar con esto. Es como un cirujano con parkinson)
            "Inviable" =  Number.null
            "Chamuyo" =  Number.false
            "Posta" =  Number.true
            "Pi" =  Number.math_PI

      Funciones:
            Cuchame()         => print()              => Imprimir en consola
            CuchameRet()      => return print         => Retorna el print
            Traeme()          => input("input str"?)  => Input en consola
            TraemeNumerito()  => input("input str"?) (int) => Input en consola (Solo numeros)
            Limpiame()        => clear console        => Limpia consola
            clear()           => clear console        => Limpia consola
            EsNumerito()      => isNumber(int)        => True si es numero, false si no
            EsTexto()         => isString(str)        => True si es string, false si no
            EsLista()         => isList([])           => True si es lista, false si no
            EsFuncion()       => isFunc(fun)          => True si es funcion, false si no
            Agregale()        => append(list, element) => Le agrega un elemento a una lista
            Rajale()          => pop(list, index)     => Le saca un elemento a una lista
            Metele()          => extend(listA,listB)  => Agrega una lista a otra
            TaLargo()         => len(list or string)  => Retorna la longitud de la lista o string
            Correme()         => run("path/file.che") => Ejecuta un archivo (Solo .che)
            Chorro()          => Probalo que esta re piola
            Argentina()       => Probalo que esta re piola
            Boludear(n)       => sleep(seconds)       => Espera n segundos
            Viborita(str)     => eval(str) => Usa python adentro de CheLang. Re pawerful. Retorna el return de python en string
            ANumerito(n-str)  => int(n-str)           => Convierte string o numero a int
            AFlotantito(n-str)=> float(n-str)         => Convierte string o numero a float
            ATextito(*)       => str(*)               => Convierte string o numero a string
            FloatYPico(n-str) => float(n-str) +- .5   => Da un float mas o menos cerca al numero
            Dolar()           => Tira el precio del dolar actual  => Tira el precio actual del dolar
            Campora()         => Probalo que esta re piola
            HalloEbribodi()   => Probalo que esta re piola
            Sumate(list[n])   => sum(list[n])         => Retorna la suma de la lista, solo numeros
            ElMasGrande()     => Probalo que esta re piola

(En ejemplos/ejemplo.che esta todo practico, se puede correr y demas)
```

## Progreso

Cualquier sugerencia o idea es bienvenida.
Tambien se aceptan Pull Requests. 
Actualmente por falta de tiempo el desarrollo esta pausado, pero si hay PR o Issues los reviso.

Este programa se crea, modifica y usa con un mate en la mano. Si no estas con un mate, anda a hacerte uno. Ya.

Se agradece la difusion de este humilde programa. Mas que nada para divertir a sus amigos. No sean ortivas.

## Disclaimer

El lenguaje no tiene intencion minima de hacer politica o estar a favor o en contra de algun partido.
Tampoco intenta ofender a nadie ni nada por el estilo. Basicamente es una gran joda. 

Si se lo toman de otra manera los invitamos a retirarse de este agradable lugar.

## Contribucion
Los Pull Requests son bienvenidos. Para cambios mayores por favor abrir un issue y ahi lo discutimo.

Antes pediamos que sea en ingles las cuestiones del PR y los issues, pero la posta es que esto es argento asi que lo vamo a seguir haciendo argento. Escriban como se les cante.

## Conducta

El que no sea respetuoso sera invitado a tomar mate con Menem mientras los lanzamos a ambos a la estratosfera.
Y una buena frase pa fomentar la organizacion: ```Si los argento nos organizamo, dominamo al mundo.``` carajo.

## Licencia
[GPLv3](https://www.gnu.org/licenses/gpl-3.0.html)

# Creditos:

[CodePulse tutorial](https://www.youtube.com/playlist?list=PLZQftyCk7_SdoVexSmwy_tBgs7P0b97yD)

[CodePulse tutorial repo](https://github.com/davidcallanan/py-myopl-code)

El tuto de CodePulse esta basado en [esto](https://ruslanspivak.com/lsbasi-part1/)

El codigo esta basado en el tuto de CodePulse con modificaciones re piolas.

Creador:
Franco Di Luciano
