function topDescription () {
	return $('.add-new-post textarea').val();
}
function mediaData () {
	return $('#upload-image').attr('src');
}
function addPost() {
	var template = `<article class="single-post">
						<div class="post-header">
							<img class="img-circle" src="https://scontent-waw1-1.xx.fbcdn.net/v/t1.0-1/p40x40/14100305_1759855060897943_7844781317309267984_n.jpg?oh=0b3187675c04f0d726e9ec3092b5dda1&oe=5A97F106">
							<p><strong>Group Name</strong> <em>share some info from</em> <strong>User Name</strong></p>
							<span class="post-time"><em>1 hour</em></span>
						</div>
						<div class="post-content">
							<div class="post-top-description">`+topDescription()+`</div>
							<div class="post-media-content"><img src="`+mediaData()+`"></div>
						</div>
						<div class="post-footer">
							<button class="btn btn-default btn-like">
								<span class="glyphicon glyphicon-thumbs-up"></span>Like
							</button>
							<button class="btn btn-default btn-comment">
								<span class="glyphicon glyphicon-edit"></span>Comment
							</button>
							<button class="btn btn-default btn-share">
								<span class="glyphicon glyphicon-share-alt"></span>Share
							</button>
						</div>
						<div class="likes-block">
							<span class="glyphicon glyphicon-thumbs-up"></span>
							<span class="likes-number">0</span>
						</div>
						<div class="post-comment">
							<img class="img-circle" src="https://scontent-waw1-1.xx.fbcdn.net/v/t1.0-1/p40x40/14100305_1759855060897943_7844781317309267984_n.jpg?oh=0b3187675c04f0d726e9ec3092b5dda1&oe=5A97F106">
							<textarea placeholder="Add some comment"></textarea>
							<div class="btn-group">
								<span class="glyphicon glyphicon-camera"></span>
								<span class="glyphicon glyphicon-user"></span>
								<span class="glyphicon glyphicon-save"></span>
							</div>
						</div>
					</article>`;
	return template;
}

function getComment (element) {
	return $(element).parents('.single-post').find('.post-comment textarea').val();
}
function addComment(cont) {
	var template = `<div class="comment">
						<div class="comment-photo">
							<img class="img-circle" src="https://scontent-waw1-1.xx.fbcdn.net/v/t1.0-1/p40x40/14100305_1759855060897943_7844781317309267984_n.jpg?oh=0b3187675c04f0d726e9ec3092b5dda1&oe=5A97F106">
						</div>
						<div class="comment-content">
							<span class="comment-author">Name Surname</span>
							<span class="author-content">`+getComment(cont)+`</span>
							<div class="comment-buttons">
								<span>Like</span>
								<span>Answer</span>
							</div>
						</div>	
					</div>`;
	return template;
}

$(document).ready(function(){
	//// addPost
	$('.btn-add-post').click(function(){
		$('.posts').prepend(addPost());
	});
	//// upload image preview
	document.getElementById("files").onchange = function () {
	    var reader = new FileReader();

	    reader.onload = function (e) {
	        // get loaded data and render thumbnail.
	        document.getElementById("upload-image").src = e.target.result;
	    };

	    // read the image file as a data URL.
	    reader.readAsDataURL(this.files[0]);

	    $('#upload-image').addClass('active');
	};
	//// likes
	$('.btn-like').click(function(){
		var currentVal = $(this).parent().next().find('.likes-number').html();
		$(this).parent().next().find('.likes-number').html( ++currentVal );
	});
	//// addComment
	$('.btn-add-comment').click(function(){
		$(this).parent().parent().parent().find(".comments").prepend(addComment(this));
		$('.post-comment textarea').val("");
	});
});
jQuery(document).ready(function(){
   $('h1').mousemove(function(e){
     var rXP = (e.pageX - this.offsetLeft-$(this).width()/2);
     var rYP = (e.pageY - this.offsetTop-$(this).height()/2);
     $('h1').css('text-shadow', +rYP/10+'px '+rXP/80+'px rgba(231, 29, 54, 1), '+rXP/70+'px '+rYP/12+'px rgba(46, 196, 182, 1)');
   });
});

