# CheLang

CheLang is an argento (Argentinian) programming language with their locals slang.

## Installation

See Releases or tags.

Downloads:

MSI Installer (with PATH. House recommendation.)

ZIP Builded

ZIP Source (requires python)

## Usage

Double click on CheLang exe

Msi installer:

open .che file

or (with PATH)

`chelang` in console


On source:
`python cli.py` in console (requires python)

## Syntax
```
Scheme:
      CheLang expression => return / regular expression
      NO CaSe SenSiTiVe keywords. Readme uses camelCase for clarity
Operations:
      ma => +
      meno => -
      por => *
      dividido => / (return float)
      aLa => **
      () => ()

      "" => "" (strings)
      [a,b,c] => [a,b,c]


ie:
      2.3 ma 2 => 4.3
      .8 ma 2 => 2.8
      .8 meno 2 => -1.2
      2 por 5 => 20
      2 aLa 2 => 4
      1 ma 2 por 3 => 9
      1 ma (2 por 3) => 7
      10 dividido 2 => 5.0

      a por 10 => "aaaaaaaaaa"

      "marado " ma "marado" => "marado marado"

      [a,b,c] + d => [a,b,c,d]
      [a,b,c] + [d,e] => [a,b,c,d,e]
      [a,b] * 3 => [a,b,a,b,a,b]
      [a,b] dividido 0 => a (change soon. will be [a,b][0] => a)


Declare variables:

      che (variable_name) es (value)
      che (variable_name) seigual (value)

      che messi es 10
      che messi es "grosso"
      che sueldo seigual 0

      messi  => 10
      sueldo => 0

Declare multiple variables:

      che (variable_name) es che (variable_2_name) es ... es (value)

      che a es che b es che c es 32

Conditions:
  (1 => true 0 => false)

      andaPor      => ==
      no es        => !=
      es nakever   => !=

      es unCachitoMeno =>   <
      es menorOIgual   =>   <=

      es unCachitoMa   =>   >
      es mayorOIgual   =>   >=

      es maomeno => +- (its equal, but return true with 20% error margin)

ie:
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
      "" anda por 1 => 0  (if string length >= 1 is true)

Conditions Combination:
      y => and / &&
      o => or / ||

      1 anda por 1 y 2 anda por 2 => 1
      1 anda por 1 y 2 anda por 1 => 0
      1 anda por 2 y 2 anda por 1 => 0

      1 anda por 1 o 2 anda por 2 => 1
      1 anda por 1 o 2 anda por 1 => 1
      1 anda por 2 o 2 anda por 1 => 0


If statement:
      ponele que => if
      tonce      => then
      oSi        => elif
      aLoSumo    => else

      ponele que messi no es 10 tonce 0 aLoSumo 1 => 1
      ponele que messi no es 9 tonce 0 aLoSumo 1  => 0

      ponele que a no es messi tonce 0 oSi a anda por a tonce 1 aLoSumo 6 => 0

      ponele que a no es a tonce 0 oSi messi anda por messi tonce 1 aLoSumo 6 => 1

For / While statement:
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

Functions:
      definime => def / function
      (a, b, c) => (a, b, c)
      => =>  () => expr (just one expr. no "hastaaca" final.)
      hastaaca => } (accept one or several expr)
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

      welcome()   (several expr (declare variable and Cuchame function))

Built-in:
      Const:
            "Milanesa" = "Carne"
            "Macri" = "Gato"
            "Vacio" =  Empty (careful. A lot of illegal operations.)
            "Inviable" =  Number.null
            "Chamuyo" =  Number.false
            "Posta" =  Number.true
            "Pi" =  Number.math_PI

      Functions:
            Cuchame()         => print()
            CuchameRet()      => return print
            Traeme()          => input("input str"?)
            TraemeNumerito()  => input("input str"?) (int)
            Limpiame()        => clear console
            clear()           => clear console
            EsNumerito()      => isNumber(int)
            EsTexto()         => isString(str)
            EsLista()         => isList([])
            EsFuncion()       => isFunc(fun)
            Agregale()        => append(list, element)
            Rajale()          => pop(list, index)
            Metele()          => extend(listA,listB)
            TaLargo()         => len(list or string)
            Correme()         => run("path/file.che")
            Chorro()          => Just try it. You must. Really. Posta.
            Argentina()       => Just try it. You must. Really. Posta.
            Boludear(n)       => sleep(seconds)
            Viborita(str)     => eval(str) => use python inside CheLang. Return python return in string
            ANumerito(n-str)  => int(n-str)
            AFlotantito(n-str)=> float(n-str)
            ATextito(*)       => str(*)
            FloatYPico(n-str) => float(n-str) +- .5

(Read example.che to more)
```


## Progress

The language IS NOT FINISHED. This is the first release. Soon upgrades.


## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

Please use english for issues and PR (unless argento words duh). Spanish are welcome too for a minor suggestion, but it will be recived with argento violence.

## Conduct

Please be respectful and dont take out the argento natura. Like they say: ```Si los argento nos organizamo, dominamo al mundo.``` 

## License
[GPLv3](https://www.gnu.org/licenses/gpl-3.0.html)

# Credits:

 [CodePulse tutorial](https://www.youtube.com/playlist?list=PLZQftyCk7_SdoVexSmwy_tBgs7P0b97yD)

   [CodePulse tutorial repo](https://github.com/davidcallanan/py-myopl-code)
    
CodePulse tutorial is based on [this](https://ruslanspivak.com/lsbasi-part1/)

The code its based on CodePulse Tutorial, with modifications.

