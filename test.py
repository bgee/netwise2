from ldModule import *
from read import auto_match1
print "began tests"

str1 = 'abcddcddf'
str2 = 'ddf'
''' should be 6'''
print find_match(str1, str2)
print "after find_match"
#exit(0)
str1 = "FRANKLINAMPYEDUCATIONBSPHDOREGONUNIVERSITY1962CHAIRDEPARTMENTOFBIOLOGYTEACHINGBIOSTATISTICSSENIORSEMINARRESEARCHENVIRONMENTALMUTAGENESISTRANSFORMATIONOFPOLLUTANTSINTOMUTAGENSSELECTEDPUBLICATIONSKHRAIWESHHMLEECMBRANDYYAKINBOYEESBERHESGITTENSGABBASMMAMPYFRASHRAFMBAKAREO2011ANTITRYPANOSOMALACTIVITIESANDCYTOTOXICITYOFSOMENOVELIMIDOSUBSTITUTED14NAPHTHOQUINONEDERIVATIVESARCHPHARMRESBREZOJCROYALFRAMPYANDVHEADINGS2006ETHNICIDENTITYANDDIABETESTYPE2HEALTHATTITUDESINAMERICANSOFAFRICANANCESTRYETHNICITYANDDISEASE16624632USTONPLJFJRURBANMASHRAFCMLEEANDFRAMPY2007L3L3ESANTIGENANDSECRETAGOGUESINDUCEHISTAMINERELEASEFROMPORCINEPERIPHERALBLOODBASOPHILSAFTERASCARISSUUMINFECTIONPARASITOLRES100603611NOUREDDINEBERKATIMIKIAVAUGHNVERLEHEADINGSBARBARAHARRISONROBERTFMURRAYJRFRANKLINRAMPYIMAMJOHARIABDULMALIK2009ATTITUDESOFMUSLIMSREGARDINGTHENEWGENETICSTESTINGTREATMENTANDTECHNOLOGYINGENETICSANDETHICSINHEALTHCARENEWQUESTIONSINTHEAGEOFGENOMICHEALTHEDRITABLACKMONSENAMERICANNURSESASSOCIATIONPP149163ROYALCDVEHEADINGSETMOLNARANDFRAMPY1995RESILIENCEINSIBLINGSOFCHILDRENWITHSICKLECELLDISEASEJGENCOUNSEL43199217AMPYFRANDAASSEFFA1988REGULATORYEFFECTSOF17BESTRADIOLONMETABOLISMOFDIMETHYLNITROSAMINEBYRENALANDHEPATICMICROSOMALENZYMESFROMBALBCMICECYTOBIOS558794AMPYFRSSAXENAANDKVERMA1988BENZOAPYRENEMUTAGENICITYINUNINDUCEDTISSUESFROMBALBCMICEANDSPRAGUEDAWLEYRATSASANINDEXOFPOSSIBLEHEALTHRISKSUSINGTHESALMONELLAMUTAGENICITYASSAYCYTOBIOS568187"
str2 = "DROSOPHILAALCOHOLDEHYDROGENASEDEVELOPMENTALSTUDIESONCRYPTICVARIANTLINES"
print find_match(str1, str2)
print auto_match(str1, str2)