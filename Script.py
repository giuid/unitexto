import sys
import os
import io
from ufal.udpipe import Model,Trainer, Pipeline, ProcessingError # pylint: disable=no-name-in-module

# In Python2, wrap sys.stdin and sys.stdout to work with unicode.
if sys.version_info[0] < 3:
    import codecs
    import locale
    encoding = locale.getpreferredencoding()
    sys.stdin = codecs.getreader(encoding)(sys.stdin)
    sys.stdout = codecs.getwriter(encoding)(sys.stdout)

if len(sys.argv) < 4:
    sys.stderr.write('Usage: %s input_format(tokenize|conllu|horizontal|vertical) output_format(conllu) model_file\n' % sys.argv[0])
    sys.exit(1)

sys.stderr.write('Loading model: ')
model = Model.load(sys.argv[3])
if not model:
    sys.stderr.write("Cannot load model from file '%s'\n" % sys.argv[3])
    sys.exit(1)
sys.stderr.write('done\n')
path="/home/guido/Progetto Unitexto/textdata/cleanedTxt/"
pipeline = Pipeline(model, sys.argv[1], Pipeline.DEFAULT, Pipeline.DEFAULT, "conllu")
sys.stderr.write('done1\n')
error = ProcessingError()
sys.stderr.write('done2\n')

i=1
tot=open("/home/guido/Progetto Unitexto/textdata/annotated1/tot.conllu", "a")
for filename in os.listdir(path):
    text=io.open(path+filename,"r", encoding="utf-8")
    string="".join(text.readlines())
    # Process data
    processed = pipeline.process(string, error)
    f = open("/home/guido/Progetto Unitexto/textdata/annotated1/"+filename[:-7]+"conllu", "a")
    if error.occurred():
        sys.stderr.write("An error occurred when running run_udpipe: ")
        sys.stderr.write(error.message)
        sys.stderr.write("\n")
        sys.exit(1)
    f.write(processed.encode("utf-8")),
    tot.write(processed.encode("utf-8"))
    tot.write("\n\n")
    
    print "File n " , i , " processed of ", len(os.listdir(path))
    i+=1
