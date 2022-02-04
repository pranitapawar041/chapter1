from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from .client_views import DownloadDocumentView

from .user_views import (LoginView, UpdateUserAdmin, UserApis, WhoAmI, ChangePassword, NotifyEmails, ActivateUser,
                         SettingOtherUserNotifyEmail, MakeAdmin, Logout)
from .client_views import ClientApis, ClientDocumentsView, ClientDetails

# TODO
# remove csrf_exempt
# after testing is done
urlpatterns = [
    path('user', UserApis.as_view()),  # TODO remove csrf_exempt
    path('user/login', LoginView.as_view()),
    path('user/logout', Logout.as_view()),
    path('user/me', WhoAmI.as_view()),
    # TODO remove csrf_exempt
    path('user/change_password', ChangePassword.as_view()),
    path('user/notify_email', NotifyEmails.as_view()),
    path('admin/user/<int:user_id>/activate', ActivateUser.as_view()),
    path('admin/user/<int:user_id>/notify_email',
         SettingOtherUserNotifyEmail.as_view()),
    path('admin/user/<int:user_id>/make_admin', MakeAdmin.as_view()),
    path('admin/user', UpdateUserAdmin.as_view()),
    path('client', ClientApis.as_view()),
    path('client/<int:client_id>/', ClientDetails.as_view()),
    path('client/<int:client_id>/document',
         ClientDocumentsView.as_view()),
    path('client/<int:client_id>/document/<int:document_id>',
         DownloadDocumentView.as_view()),
]
