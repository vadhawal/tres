
from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
from mezzanine.core.views import direct_to_template
from django.conf.urls.defaults import *
from django.contrib.comments.models import Comment
from voting.views import vote_on_object
from imagestore.models import Album, Image
from hitcount.views import update_hit_count_ajax
from mezzanine.generic.models import ThreadedComment
from userProfile.views import close_login_popup
from userProfile.views import broadcast

comment_dict = {
    'model': ThreadedComment,
    'template_object_name': 'comment',
    'slug_field': 'slug',
    'allow_xmlhttprequest': 'true',    
}
album_dict = {
    'model': Album,
    'template_object_name': 'album',
    'slug_field': 'slug',
    'allow_xmlhttprequest': 'true',
}
image_dict = {
    'model': Image,
    'template_object_name': 'image',
    'slug_field': 'slug',
    'allow_xmlhttprequest': 'true',
}

admin.autodiscover()

# Add the urlpatterns for any custom Django applications here.
# You can also change the ``home`` view to add your own functionality
# to the project's homepage.

urlpatterns = patterns("",
    url(r'', include('social_auth.urls')),
    url(r'^relationships/', include('relationships.urls')),
    ('^activity/', include('actstream.urls')),
    # Change the admin prefix here to use an alternate URL for the
    # admin interface, which would be marginally more secure.
    ("^admin/", include(admin.site.urls)),
    url(r'^comments/(?P<object_id>\d+)/(?P<direction>up|down|clear)/vote/?$', vote_on_object, comment_dict),
    url(r'^albums/(?P<object_id>\d+)/(?P<direction>up|down|clear)/vote/?$', vote_on_object, album_dict),
    url(r'^images/(?P<object_id>\d+)/(?P<direction>up|down|clear)/vote/?$', vote_on_object, image_dict),  
    url(r'^voters/(?P<content_type_id>\d+)/(?P<object_id>\d+)/$', 'voting.views.get_voters_info', name='get_voters_info'), 
    (r"^gallery/", include("imagestore.urls", namespace="imagestore")),
    url(r'^object/hit/$', update_hit_count_ajax, name='hitcount_update_ajax'),
    url(r'^close_login_popup/$', close_login_popup, name='login_popup_close'),
    url(r'^find-friends/', include('social_friends_finder.urls')),
    (r'^messages/', include('django_messages.urls')),
    url(r'^notification/', include('notification.urls')),
    url(r'^broadcast/', broadcast, name="broadcast" ),
    url('^', include('follow.urls')),
    # We don't want to presume how your homepage works, so here are a
    # few patterns you can use to set it up.

    # HOMEPAGE AS STATIC TEMPLATE
    # ---------------------------
    # This pattern simply loads the index.html template. It isn't
    # commented out like the others, so it's the default. You only need
    # one homepage pattern, so if you use a different one, comment this
    # one out.

    url("^$", direct_to_template, {"template": "index.html"}, name="home"),
    # HOMEPAGE AS AN EDITABLE PAGE IN THE PAGE TREE
    # ---------------------------------------------
    # This pattern gives us a normal ``Page`` object, so that your
    # homepage can be managed via the page tree in the admin. If you
    # use this pattern, you'll need to create a page in the page tree,
    # and specify its URL (in the Meta Data section) as "/", which
    # is the value used below in the ``{"slug": "/"}`` part. Make
    # sure to uncheck all templates for the "show in menus" field
    # when you create the page, since the link to the homepage is
    # always hard-coded into all the page menus that display navigation
    # on the site. Also note that the normal rule of adding a custom
    # template per page with the template name using the page's slug
    # doesn't apply here, since we can't have a template called
    # "/.html" - so for this case, the template "pages/index.html" can
    # be used.

    # url("^$", "mezzanine.pages.views.page", {"slug": "/"}, name="home"),

    # HOMEPAGE FOR A BLOG-ONLY SITE
    # -----------------------------
    # This pattern points the homepage to the blog post listing page,
    # and is useful for sites that are primarily blogs. If you use this
    # pattern, you'll also need to set BLOG_SLUG = "" in your
    # ``settings.py`` module, and delete the blog page object from the
    # page tree in the admin if it was installed.

    # url("^$", "mezzanine.blog.views.blog_post_list", name="home"),

    # MEZZANINE'S URLS
    # ----------------
    # ADD YOUR OWN URLPATTERNS *ABOVE* THE LINE BELOW.
    # ``mezzanine.urls`` INCLUDES A *CATCH ALL* PATTERN
    # FOR PAGES, SO URLPATTERNS ADDED BELOW ``mezzanine.urls``
    # WILL NEVER BE MATCHED!

    # If you'd like more granular control over the patterns in
    # ``mezzanine.urls``, go right ahead and take the parts you want
    # from it, and use them directly below instead of using
    # ``mezzanine.urls``.
    ("^", include("mezzanine.urls")),

    # MOUNTING MEZZANINE UNDER A PREFIX
    # ---------------------------------
    # You can also mount all of Mezzanine's urlpatterns under a
    # URL prefix if desired. When doing this, you need to define the
    # ``SITE_PREFIX`` setting, which will contain the prefix. Eg:
    # SITE_PREFIX = "my/site/prefix"
    # For convenience, and to avoid repeating the prefix, use the
    # commented out pattern below (commenting out the one above of course)
    # which will make use of the ``SITE_PREFIX`` setting. Make sure to
    # add the import ``from django.conf import settings`` to the top
    # of this file as well.
    # Note that for any of the various homepage patterns above, you'll
    # need to use the ``SITE_PREFIX`` setting as well.

    # ("^%s/" % settings.SITE_PREFIX, include("mezzanine.urls"))

)

# Adds ``STATIC_URL`` to the context of error pages, so that error
# pages can use JS, CSS and images.
handler404 = "mezzanine.core.views.page_not_found"
handler500 = "mezzanine.core.views.server_error"
