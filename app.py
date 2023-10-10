from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

comments = {
        '1': {'user_id': '1', 'post_id':'2','comment':'Amazing post!'},
        '2': {'user_id': '2', 'post_id':'2','comment':'I did not know that'}
    }


#get all comments
@app.route('/comment',methods=['GET'])
def get_all_comments():
    allcomments = comments
    for i in allcomments:
        response = requests.get(f'http://localhost:5001/post/{allcomments[i]["post_id"]}')
        if response.status_code == 200:
            allcomments[i]['posts'] = response.json()
        response = requests.get(f'http://localhost:5000/user/{allcomments[i]["user_id"]}')
        if response.status_code == 200:
            allcomments[i]['user'] = response.json()
    
    return jsonify(allcomments)


#get speific comment with post and user information
@app.route('/comment/<id>' , methods=['GET'])
def get_comment(id):
    if id in comments:
        comment_info = comments.get(id,{})
        print(comment_info)
        if comment_info:
            response = requests.get(f'http://localhost:5001/post/{comment_info["post_id"]}')
            if response.status_code == 200:
                comment_info['post'] = response.json()
            response = requests.get(f'http://localhost:5000/user/{comment_info["user_id"]}')
            if response.status_code == 200:
                comment_info['comment_user'] = response.json()
            return jsonify(comment_info)
        else:
            return {"error": "Comment does not exist"}


#create comment
@app.route('/comment', methods=['POST'])
def create_post():
    newId = (len(comments)+1)
    new_comment = {
        str(newId ):  { 'user_id':request.json['user_id'], "post_id": request.json["post_id"], 'comment':request.json["comment"]}
            }
    comments.update(new_comment)
    return new_comment


#update comment
@app.route('/comment/<id>', methods=['PUT'])
def update_comment(id):    
    if id in comments:
        update_comment = {'user_id':comments[id]['user_id'], 'post_id':comments[id]['post_id'],'comment':request.json["comment"]}
        comments.update({id:update_comment})
        return update_comment
    else:
        return {'error':'User Not Found'}
    

#delete comment
@app.route('/comment/<id>',methods=['DELETE'])
def delete_comment(id):
    if id in comments:
        del comments[id]
        return comments
    else:
       return {'error': 'User Does Not Exist'}


if __name__ == '__main__':
    app.debug = True
    app.run(port=5002)