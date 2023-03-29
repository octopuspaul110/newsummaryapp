from flask import Flask,jsonify,request,make_response
from rouge import Rouge
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer
import openai

openai.api_key = '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'
app = Flask(__name__)
@app.route('/api/get_summy_summary_textrank',methods = ['POST'])
def get_summy_summary_textrank():
    try:
        data = request.get_json()
        if data is None:
            return make_response(jsonify(dict(message = 'invalid request')),400)
        content = data.get('content')
        if content is None or len(content) < 100:
            return make_response(jsonify(dict(message = 'invalid request')),400)
        parser = PlaintextParser.from_string(content, Tokenizer("english"))
        summarizer = LexRankSummarizer()
        summary = summarizer(parser.document, 3)
        result = ""
        for words in summary:
            result += str(words)
        return jsonify({'message':'success','summary':result,'Rouge_score':Rouge_score(content,result)})
    except Exception as e:
        return jsonify({'message':f'error {str(e)}'})
#for lunh summarizer
@app.route('/api/get_summy_lunh',methods = ['POST'])
def get_summy_lunh():
    from sumy.summarizers.luhn import LuhnSummarizer
    try:
        data = request.get_json()
        if data is None:
            return make_response(jsonify(dict(message = 'invalid request')),400)
        content = data.get('content')
        if content is None or len(content) < 100:
            return make_response(jsonify(dict(message = 'invalid request')),400)
        parser = PlaintextParser.from_string(content, Tokenizer("english"))
        summarizer = LuhnSummarizer()
        summary = summarizer(parser.document, 3)
        result = ""
        for words in summary:
            result += str(words)
        return jsonify({'message':'success','summary':result,'Rouge_score':Rouge_score(content,result)})
    except Exception as e:
        return jsonify({'message':f'error {str(e)}'})
@app.route('/api/get_summy_lsa',methods = ['POST'])
def get_summy_lsa():
    from sumy.summarizers.lsa import LsaSummarizer
    try:
        data = request.get_json()
        if data is None:
            return make_response(jsonify(dict(message = 'invalid request')),400)
        content = data.get('content')
        if content is None or len(content) < 100:
            return make_response(jsonify(dict(message = 'invalid request')),400)
        parser = PlaintextParser.from_string(content, Tokenizer("english"))
        summarizer = LsaSummarizer()
        summary = summarizer(parser.document, 3)
        result = ""
        for words in summary:
            result += str(words)
        return jsonify({'message':'success','summary':result,'Rouge_score':Rouge_score(content,result)})
    except Exception as e:
        return jsonify({'message':f'error {str(e)}'})
@app.route('/api/get_summy_lex',methods = ['POST'])
def get_summy_lex():
    from sumy.summarizers.lex_rank import LexRankSummarizer
    try:
        data = request.get_json()
        if data is None:
            return make_response(jsonify(dict(message = 'invalid request')),400)
        content = data.get('content')
        if content is None or len(content) < 100:
            return make_response(jsonify(dict(message = 'invalid request')),400)
        parser = PlaintextParser.from_string(content, Tokenizer("english"))
        summarizer = LexRankSummarizer()
        summary = summarizer(parser.document, 3)
        result = ""
        for words in summary:
            result += str(words)
        return jsonify({'message':'success','summary':result,'Rouge_score':Rouge_score(content,result)})
    except Exception as e:
        return jsonify({'message':f'error {str(e)}'})
@app.route('/api/get_openai_summary',methods = ['POST'])
def get_openai_summary():
    #text = request.args.get('text')
    #summary_lenght = request.get_json()
    #if summary_lenght:
    #    summary_lenght = summary_lenght.get('summary_lenght')
    #    summary_lenght = int(summary_lenght)
    try:
        #print(pickle.dump(request))
        data = request.get_json()
        if data is None:
            return make_response(jsonify(dict(message = 'invalid request')),400)
        content = data.get('content')
        if content is None or len(content) < 100:
            return make_response(jsonify(dict(message = 'invalid request')),400)
        summary = get_summary(prompt = content,max_tokens = 200)
        return jsonify({'message':'success','summary':summary,'Rouge_score':Rouge_score(content,summary)})
    except Exception as e:
        return jsonify({'message':f'error {str(e)}'})
    '''else:
        try:
            #print(pickle.dump(request))
            data = request.get_json()
            if data is None:
                return make_response(jsonify(dict(message = 'invalid request')),400)
            content = data.get('content')
            if content is None or len(content) < 100:
                return make_response(jsonify(dict(message = 'invalid request')),400)

            summary = get_summary(prompt = content,max_tokens = 200)#the default tokens is 200 except the user demands more
            return jsonify({'message':'success','summary':summary,'Rouge_score':Rouge_score(content,summary)})
        except Exception as e:
            return jsonify({'message':f'error {str(e)}'})'''
def get_summary(prompt,max_tokens):
    response = openai.Completion.create(
            model ="text-davinci-003",
            #engine="davinci",
            prompt='summarize this for an intelligent person:\n' + prompt,
            temperature=0.7,
            max_tokens=max_tokens,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
    return response["choices"][0]["text"]
def Rouge_score(reference,candidate):
    Rouger = Rouge()
    return Rouger.get_scores(reference,candidate)
if __name__ == '__main__':
    app.run(debug = True)