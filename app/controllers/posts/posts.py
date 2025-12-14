from flask import (
    Blueprint,
    get_flashed_messages,
    render_template,
    request,
    redirect,
    url_for,
    session,
    flash,
)
import models.posts.post as Post
import models.posts.comment as Comment
import models.posts.tag as Tag
import models.users.user as User
from controllers.posts.moderation import analyze_text

postfeed_bp = Blueprint("postfeed", __name__)


@postfeed_bp.route("/", methods=["GET"])
def postfeed():
    tag_filter = (request.args.get("tags") or "").strip()
    tags = (
        list({t.strip() for t in tag_filter.split(",") if t.strip()})
        if tag_filter
        else []
    )

    last = request.args.get("last") or None

    limit = 10
    posts = Post.get_posts(limit=limit + 1, tags=tags, last_retrieved=last)
    if isinstance(posts, str):
        flash(f"Error retrieving posts: {posts}", "error")
        posts = []

    has_more = len(posts) > limit
    posts_to_render = posts[:limit]

    for post in posts_to_render:
        tag_rows = Tag.get_tags_for_post(post["id"])
        if isinstance(tag_rows, str):
            flash(
                f"Error retrieving tags for post ID {post['id']}: {tag_rows}", "error"
            )
            post["tags"] = []
        else:
            post["tags"] = [t["name"] for t in tag_rows]

    next_last = None
    if has_more and posts_to_render:
        ca = posts_to_render[-1]["created_at"]
        next_last = (
            ca.isoformat() if hasattr(ca, "isoformat") else str(ca).split(".")[0]
        )

    return render_template(
        "posts/postfeed.html",
        posts=posts_to_render,
        role=session.get("role", "guest"),
        tags_query=tag_filter,
        next_last=next_last,
        has_more=has_more,
    )


createpost_bp = Blueprint("createpost", __name__)


@createpost_bp.route("/create", methods=["GET", "POST"])
def create_post():
    if request.method == "POST":
        if session.get("role") == "guest" or not session.get("username"):
            flash("You must be logged in to comment", "error")
            return redirect(url_for("login.login"))

        content = request.form["content"]
        text_color = request.form["text_color"]
        text_font_id = request.form["text_font"]
        username = session.get("username")
        if not username:
            flash("You must be logged in to create a post.", "error")
            return redirect(url_for("createpost.create_post"))
        user = User.get_data(username, ["id"])
        if isinstance(user, str):
            flash(f"Error retrieving user data: {user}", "error")
            return redirect(url_for("createpost.create_post"))
        user_id = user["id"]

        tags_input = request.form.get("tags", "")
        tags = [tag.strip() for tag in tags_input.split(",") if tag.strip()]
        tags = list(set(tags))

        if err := Post.check_length("content", content):
            flash(f"Content must be between {err} characters.", "error")
        if not analyze_text(content, threshold=2):
            flash(
                "Content violates safety policies. Please modify and try again.",
                "error",
            )
            return redirect(url_for("createpost.create_post"))

        if err := Post.check_length("text_color", text_color):
            flash(f"Text color must be between {err} characters.", "error")

        for tag in tags:
            if err := Tag.check_length("name", tag):
                flash(f"Tag '{tag}' must be between {err} characters.", "error")

        if len(get_flashed_messages(category_filter=["error"])) > 0:
            flash("Please correct the errors and try again.", "error")
            return redirect(url_for("createpost.create_post"))

        tag_ids = []
        for tag in tags:
            if not Tag.check_exists(tag):
                tag_id = Tag.add(tag, date=None)
                if not tag_id or isinstance(tag_id, str):
                    flash(f"Error adding tag '{tag}': {tag_id}", "error")
                    return redirect(url_for("createpost.create_post"))
                tag_ids.append(tag_id)
            else:
                tag_id = Tag.get_tag_id(tag)
                if tag_id:
                    tag_ids.append(tag_id)

        post_id = Post.add_post(user_id, content, text_color, text_font_id)
        if isinstance(post_id, str):
            flash(f"Error creating post: {post_id}", "error")
            return redirect(url_for("createpost.create_post"))

        for tag_id in tag_ids:
            if err := Tag.add_post_tag(post_id, tag_id):
                flash(f"Error associating tag ID {tag_id} with post: {err}", "error")
                return redirect(url_for("createpost.create_post"))

        return redirect(url_for("viewpost.view_post", post_id=int(post_id)))
    fonts = Post.get_text_fonts()
    return render_template(
        "posts/createpost.html",
        role=session.get("role", "guest"),
        fonts=fonts,
    )


viewpost_bp = Blueprint("viewpost", __name__)


@viewpost_bp.route("/<int:post_id>", methods=["GET", "POST"])
def view_post(post_id):
    post = Post.get_post(int(post_id))
    if not post or isinstance(post, str):
        flash(f"Post not found. id = {post_id}, {post}", "error")
        return redirect(url_for("postfeed.postfeed"))

    no_inc = request.args.get("no_view_inc") == "1"
    if request.method == "GET" and not no_inc:
        Post.increase_views(int(post_id))
        post["views"] += 1

    comments = Comment.get_comments(int(post_id))
    if isinstance(comments, str):
        flash(f"Error retrieving comments: {comments}", "error")
        comments = []

    tags = Tag.get_tags_for_post(int(post_id))
    if isinstance(tags, str):
        flash(f"Error retrieving tags: {tags}", "error")
        tags = []
    post["tags"] = [tag["name"] for tag in tags]

    if request.method == "POST":
        if session.get("role") == "guest" or not session.get("username"):
            flash("You must be logged in to comment.", "error")
            return redirect(url_for("login.login"))

        comment_text = request.form.get("comment_text", "").strip()
        if not comment_text:
            flash("Comment cannot be empty.", "error")
            return redirect(
                url_for("viewpost.view_post", post_id=post_id, no_view_inc=1)
            )
        if err := Comment.check_length("content", comment_text):
            flash(f"Comment must be between {err} characters.", "error")
            return redirect(
                url_for("viewpost.view_post", post_id=post_id, no_view_inc=1)
            )
        if not analyze_text(comment_text, threshold=2):
            flash(
                "Comment violates safety policies. Please modify and try again.",
                "error",
            )
            return redirect(
                url_for("viewpost.view_post", post_id=post_id, no_view_inc=1)
            )

        username = session.get("username")
        user = User.get_data(username, ["id"])
        if isinstance(user, str) or not user:
            flash("User not found.", "error")
            return redirect(
                url_for("viewpost.view_post", post_id=post_id, no_view_inc=1)
            )

        user_id = user["id"]
        err = Comment.add_comment(post_id, user_id, comment_text)
        if err:
            flash(f"Error adding comment: {err}", "error")
        else:
            flash("Comment added successfully.", "success")

        return redirect(url_for("viewpost.view_post", post_id=post_id, no_view_inc=1))

    return render_template(
        "posts/viewpost.html",
        post=post,
        comments=comments,
        role=session.get("role", "guest"),
    )


@viewpost_bp.route("/<int:post_id>/delete", methods=["POST"])
def delete_post(post_id):
    post = Post.get_post(post_id)
    tags = Tag.get_tags_for_post(post_id)
    if not post or isinstance(post, str):
        flash("Post not found.", "error")
        return redirect(url_for("postfeed.postfeed"))
    if session.get("role") != "admin" and session.get("username") != post["username"]:
        flash("You do not have permission to delete this post.", "error")
        return redirect(url_for("viewpost.view_post", post_id=post_id))
    Post.remove_post(post_id)
    flash("Post deleted.", "success")
    for tag in tags:
        associated_posts = Post.get_posts(tags=[tag["name"]])
        if isinstance(associated_posts, str):
            continue
        if len(associated_posts) == 0:
            Tag.delete_tag(tag["id"])
    return redirect(url_for("postfeed.postfeed"))


@viewpost_bp.route("/<int:post_id>/comment/<int:comment_id>/delete", methods=["POST"])
def delete_comment(post_id, comment_id):
    comment = Comment.get_comment(comment_id)
    if not comment or isinstance(comment, str):
        flash("Comment not found.", "error")
        return redirect(url_for("viewpost.view_post", post_id=post_id, no_view_inc=1))
    if session.get("role") != "admin" and session.get("username") != comment["author"]:
        flash("You do not have permission to delete this comment.", "error")
        return redirect(url_for("viewpost.view_post", post_id=post_id, no_view_inc=1))
    Comment.remove_comment(comment_id)
    flash("Comment deleted.", "success")
    return redirect(url_for("viewpost.view_post", post_id=post_id, no_view_inc=1))
