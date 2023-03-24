from flask import Flask,jsonify,request,make_response
import openai
from rouge import Rouge

openai.api_key = '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'
app = Flask(__name__)

def get_summary(prompt,max_tokens):
    response = openai.Completion.create(engine="davinci",prompt=prompt,temperature=0.3,
            max_tokens=max_tokens,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
    return response["choices"][0]["text"]

@app.route('/api/summarizer',methods = ['POST'])
def summarizer():
    text = request.ars.get('text')
    summary_lenght = request.args.get('summary_lenght')
    if summary_lenght:
        summary_lenght = int(summary_lenght)
        try:
            #print(pickle.dump(request))
            data = request.get_json()
            if data is None:
                return make_response(jsonify(dict(message = 'invalid request')),400)
            content = data.get('content')
            if content is None or len(content) < 100:
                return make_response(jsonify(dict(message = 'invalid request')),400)

            summary = get_summary(prompt = content,max_tokens = summary_lenght)
            return jsonify({'message':'success','summary':summary,'Rouge_score':Rouge_score(content,summary)})
        except Exception as e:
            return jsonify({'message':f'error {str(e)}'})
    else:
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
            return jsonify({'message':f'error {str(e)}'})
def Rouge_score(reference,candidate):
    Rouger = Rouge()
    return Rouger.get_scores(reference,candidate)


if __name__ == '__main__':
    app.run(debug=True)