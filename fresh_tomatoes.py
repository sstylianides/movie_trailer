import webbrowser
import os
import re


# Styles and scripting for the page
main_page_head = '''
<!DOCTYPE html>
<html lang="en">
<head>

    <meta charset="utf-8">
    <title>Extra Fresh Movie Trailers!</title>

    <!-- Bootstrap 3 -->
    <link rel="stylesheet" href="css/main.css">
    <link rel="stylesheet" href="https://netdna.bootstrapcdn.com/bootstrap/3.1.0/css/bootstrap.min.css">
    <link rel="stylesheet" href="https://netdna.bootstrapcdn.com/bootstrap/3.1.0/css/bootstrap-theme.min.css">
    <script src="http://code.jquery.com/jquery-1.10.1.min.js"></script>
    <script src="https://netdna.bootstrapcdn.com/bootstrap/3.1.0/js/bootstrap.min.js"></script>

    <script type="text/javascript" charset="utf-8">
        // Pause the video when the modal is closed
        $(document).on('click', '.hanging-close, .modal-backdrop, .modal', function (event) {
            // Remove the src so the player itself gets removed, as this is the only
            // reliable way to ensure the video stops playing in IE
            $("#trailer-video-container").empty();
        });
        // Start playing the video whenever the trailer modal is opened
        $(document).on('click', '.movie-tile', function (event) {
            var trailerYouTubeId = $(this).attr('data-trailer-youtube-id')
            var sourceUrl = 'http://www.youtube.com/embed/' + trailerYouTubeId + '?autoplay=1&html5=1';
            $("#trailer-video-container").empty().append($("<iframe></iframe>", {
              'id': 'trailer-video',
              'type': 'text-html',
              'src': sourceUrl,
              'frameborder': 0
            }));
        });
        // Animate in the movies when the page loads
        $(document).ready(function () {
          $('.movie-tile').hide().first().show("fast", function showNext() {
            $(this).next("div").show("fast", showNext);
          });
        });
    </script>
</head>
'''


# The main page layout and title bar
main_page_content = '''
  <body>
    <!-- Trailer Video Modal -->
    <div class="modal" id="trailer">
      <div class="modal-dialog">
        <div class="modal-content">
          <a href="#" class="hanging-close" data-dismiss="modal" aria-hidden="true">
            <img src="https://lh5.ggpht.com/v4-628SilF0HtHuHdu5EzxD7WRqOrrTIDi_MhEG6_qkNtUK5Wg7KPkofp_VJoF7RS2LhxwEFCO1ICHZlc-o_=s0#w=24&h=24"/>
          </a>
          <div class="scale-media" id="trailer-video-container">
          </div>
        </div>
      </div>
    </div>

    <!-- Main Page Content -->
     <div class="navbar navbar-default navbar-custom navbar-fixed-top">
  <div class="container">
    <div class="navbar-header">
      <button type="button" class="navbar-toggle" data-toggle="collapse" data-target=".navbar-collapse">
        <span class="icon-bar"></span>
        <span class="icon-bar"></span>
        <span class="icon-bar"></span>
      </button>
      <a class="navbar-brand brand-name" href="fresh_tomatoes.html">Extra Fresh Movie Trailers</a>
    </div>
    <div class="collapse navbar-collapse">
      <ul class="nav navbar-nav"></ul>
    </div><!--/.nav-collapse -->
  </div>
</div>
      {movie_tiles}
    <footer>

<div id="footer">
    <div class="container">
        <div class="row">
            <h3 class="footertext">Get in Touch With Stephan Stylianides:</h3>
            <br>
              <div class="col-md-4">
                <center>
                  <a href="https://www.linkedin.com/in/stephan-stylianides-768b3174" target="_blank">
                  <img src="images/Linkedin_icon.png" alt="LinkedIn Logo">
                  <br>
                  <h4 class="footertext">Connect with me on LinkedIn</h4>
                  <p class="footertext"><br>
                  </a>
                </center>
              </div>
              <div class="col-md-4">
                <center>
                  <a href="http://www.stephanstylianides.com" target="_blank">
                  <img src="images/www.png" alt="World Wide Web Logo">
                  <br>
                  <h4 class="footertext">Check out my portfolio website</h4>
                  <p class="footertext"><br>
                  </a>
                </center>
              </div>
              <div class="col-md-4">
                <center>
                  <a href="https://github.com/sstylianides?tab=repositories" target="_blank">
                  <img src="images/GitHub_Logo.png" class="img-circle" alt="GitHub Logo">
                  <br>
                  <h4 class="footertext">Browse my GitHub Repositories</h4>
                  <p class="footertext"><br>
                  </a>
                </center>
              </div>
            </div>
            <div class="row">
            <p><center><a href="mailto:stephan.stylianides@gmail.com">Click here to send me an email</a> <p class="footertext">Copyright 2017</p></center></p>
        </div>
    </div>
</div>
</footer>
  </body>
</html>
'''


# A single movie entry html template
movie_tile_content = '''
<div class="col-md-6 col-lg-4 movie-tile text-center" data-trailer-youtube-id="{trailer_youtube_id}" data-toggle="modal" data-target="#trailer">
    <img src="{poster_image_url}" width="400" height="600">
    <div class="title-info">
    <h2>{movie_title}</h2>
    <div class="info-box">{movie_storyline}</div>
    <br>
    <a class"btn btn-primary" role="button" href="{movie_website}" target="_blank">IMDb Website</a>
</div>
</div>
'''


def create_movie_tiles_content(movies):
    # The HTML content for this section of the page
    content = ''
    for movie in movies:
        # Extract the youtube ID from the url
        youtube_id_match = re.search(
            r'(?<=v=)[^&#]+', movie.trailer_youtube_url)
        youtube_id_match = youtube_id_match or re.search(
            r'(?<=be/)[^&#]+', movie.trailer_youtube_url)
        trailer_youtube_id = (youtube_id_match.group(0) if youtube_id_match
                              else None)

        # Append the tile for the movie with its content filled in
        content += movie_tile_content.format(
            movie_title=movie.title,
            poster_image_url=movie.poster_image_url,
            trailer_youtube_id=trailer_youtube_id,
            movie_storyline=movie.storyline,
            movie_website=movie.website_url
        )
    return content


def open_movies_page(movies):
    # Create or overwrite the output file
    output_file = open('fresh_tomatoes.html', 'w')

    # Replace the movie tiles placeholder generated content
    rendered_content = main_page_content.format(
        movie_tiles=create_movie_tiles_content(movies))

    # Output the file
    output_file.write(main_page_head + rendered_content)
    output_file.close()

    # open the output file in the browser (in a new tab, if possible)
    url = os.path.abspath(output_file.name)
    webbrowser.open('file://' + url, new=2)
