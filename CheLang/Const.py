import string
###################################################
# CONSTANTS - me dijeron que significa constantes -
###################################################

DIGITS = "0123456789" # los numerito
LETTERS = string.ascii_letters + "ñÑ"
LETTERS_DIGITS = LETTERS + DIGITS

###################################################
# ERRORS                            - bad news D: -
###################################################
###############################
# ERROR MESSAGES     - sfw :D -
###############################
# violentitud : media
errorMessages = {
    "IllegalCharError" : "Che pibe pusiste algo nada que ver, le mandaste",
    "InvalidSyntaxError" : "Flaco tu sintaxis no la entiende ni tu abuelita (saludos)",
    "RuntimeError" : "TE VAMOS A LINCHAR SI NO LO ARREGLAS BIGOTE",
    "ExpectedCharError" : "Usted se tiene que arrepentir de lo que dijo. Le faltó poner algo: ",
    "languageThings": "Te tiro un dato: estas en CheLang. Argentina. Te controla el gobierno"
}
###############################
# ERROR DETAILS     - sfw :D -
###############################
detailsMessages = {
    "intOrFloatExpected" : "\nFlaco pasame un numerito ahi viste",
    "exprExpected" : "\nFlaco pasame un algo ahi viste",
    "operationExpected": "\nFlaco dame alguna operacion, lamentablemente no puedo hacer lo que me pinte",
    "closeParentesisExpected": "\nFlaco porque no cerras los partentesis?",
    "identifierExpected": "\nDecime un nombre pa la variable viste",
    "equalExpected": "\nTenes que poner 'es' o 'seigual' o 'son' pa poner algo crack",
    "equalAfterNotExpected": "\nChe no sabes español? Tenes que poner 'No es' duh",
    "zeroDiv": "\nIntenté dividir por 0, pero no pude por culpa del kernel imperialista",
    "unknownVariable": "\nCapo no me dijiste que es '",
    "languajeSyntaxError": "\nGenio leete la doc antes de escribir dale? Te faltó un '",
    "outOfIndex": "\nTe pasaste de rosca con el index capo",
    "dolarVarAssign": "\n\nJA! Quien te crees que sos para cambiarle el valor al dolar? Eso lo controla el Banco Central capo."
}

###############################
# TOKENS TYPES
###############################
TT_INT = "TT_INT"
TT_FLOAT = "FLOAT"
TT_STRING = "STRING"
TT_IDENTIFIER = "IDENTIFIER"
TT_KEYWORD = "KEYWORD"
TT_PLUS = "PLUS"
TT_MINUS = "MINUS"
TT_MUL = "MUL"
TT_DIV = "DIV"
TT_POW = "POW"
TT_EQ = "EQ"
TT_LPAREN = "LPAREN"
TT_RPAREN = "RPAREN"
TT_LSQUARE = "LSQUARE"
TT_RSQUARE = "RSQUARE"
TT_EE = "EE"
TT_MM = "MM"
TT_NE = "NE"
TT_LT = "LT"
TT_GT = "GT"
TT_LTE = "LTE"
TT_GTE = "GTE"
TT_COMMA = "COMMA"
TT_ARROW = "ARROW"
TT_NEWLINE = "NEWLINE"
TT_EOF = "EOF"

###############################
# KEYWORDS
###############################
KEYWORDS = [
    "che",
    "y",
    "o",
    "no",
    "ponele",
    "tonce",
    "osi",
    "alosumo",
    "agarra",
    "hasta",
    "de",
    "mientras",
    "definime",
    "hastaaca",
    "tirame",
    "segui",
    "piquete"
]