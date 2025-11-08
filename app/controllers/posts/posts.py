from flask import Blueprint, render_template, request, redirect, url_for, session
import models.posts.post as Post
import models.posts.comment as Comment

postfeed_bp = Blueprint('postfeed', __name__)

@postfeed_bp.route('/')
def postfeed():
    posts = Post.get_all_posts()
    return render_template('posts/postfeed.html', posts=posts, role=session.get('role', 'guest'))

createpost_bp = Blueprint('createpost', __name__)

@createpost_bp.route('/create', methods=['GET', 'POST'])
def create_post():
    if request.method == 'POST':
        text = request.form['content']
        text_color = request.form['text_color']
        text_font = request.form['text_font']
        author = session.get('username', 'guest')
        post_id = Post.add_post(text, text_color, text_font, author)
        return redirect(url_for('viewpost.view_post', post_id=post_id))
    return render_template('posts/createpost.html', role=session.get('role', 'guest'))

viewpost_bp = Blueprint('viewpost', __name__)

@viewpost_bp.route('/<int:post_id>', methods=['GET', 'POST'])
def view_post(post_id):
    post = Post.get_post_by_id(int(post_id))
    if not post:
        return "Post not found", 404

    comments = Comment.get_comments_by_post_id(int(post_id))

    if request.method == 'POST':
        comment_text = request.form['comment_text']
        author = session.get('username', 'guest')
        Comment.add_comment(comment_text, author, int(post_id))
        return redirect(url_for('viewpost.view_post', post_id=post_id))

    return render_template('posts/viewpost.html', post=post, comments=comments, role=session.get('role', 'guest'))

