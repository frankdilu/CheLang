# CheLang

CheLang is an argento (Argentinian) programming language with their locals says.

## Installation

For now, just clone the repo. Working in it.


## Usage

Console:
python shell.py

```
Scheme:
      CheLang expression => return / regular expression

Operations:
      ma => +
      meno => -
      por => +
      dividido => /
      ala => **
      () => ()

ie:
       2 ma 2 => 4
       2 por 5 => 20
       2 ala 2 => 4
       1 ma 2 por 3 => 9
       1 ma (2 por 3) => 7


Declare variables:

    che (variable_name) es (value. just numbers for now)

    che messi es 10

    messi => 10

Declare multiple variables:

     che (variable_name) es che (variable_2_name) es ... es (value. just numbers for now)
            
     che a es che b es che c es 32

Conditions:
  (1 => true 0 => false)

      andaPor   => ==
      no es   => !=
      es nakever   => !=

      es unCachitoMeno   => <
      es menorOIgual   => <=
            
      es unCachitoMa   => >
      es mayorOIgual   => >=

      es maomeno => +- (its equal, but return true with 20% error margin)

ie:
      1 andaPor 1 => 1
      a andaPor 1 => 0
      a andaPor 32 => 1
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

Conditions Combination:
      y => and / &&
      o => or / ||

      1 andaPor 1 y 2 andaPor 2 => 1
      1 andaPor 1 y 2 andaPor 1 => 0
      1 andaPor 2 y 2 andaPor 1 => 0

      1 andaPor 1 o 2 andaPor 2 => 1
      1 andaPor 1 o 2 andaPor 1 => 1
      1 andaPor 2 o 2 andaPor 1 => 0
```

## Progress

The language IS NOT FINISHED. Any help is helpful. This is the beta of the beta of the beta. Or, doing maths, .5Alpha.


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

