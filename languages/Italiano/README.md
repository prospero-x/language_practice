## verb_getter.VerbGetter

VerbGetter is the implementation of the required interface VerbInterface for this program.
 When a verb is requested, VerbGetter first looks for the verb in the verbstore/verbs.json.
If it cannot find it there, the VerbGetter will get the conjugations from
 http://www.italian-verbs.com/italian-verbs/conjugation.php?parola=<verb_name>. As soon as 
 the verb's conjugations are downloaded, they will be saved to verbstore/verbs.json.
 
 If VerbGetter can't find the verb at the link above, an error will be raised.
 
 The download script has a global variable VERB_CATEGORIES which **must** contain the
 same tense names as VerbGetter.tenses.

 ## Developer

 Do not commit any files under verbstore/ to github! VerbGetter will take care of all 
 necessary downloads.

