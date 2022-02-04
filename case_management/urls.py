from django.urls import path
from case_management.timeline_views import TimeLineEntryView, TimelineSingleEntryView
from case_management.views import (CaseDocumentsView, CaseView, ClientCaseView, ContactView,
                                   DownloadDocumentView)

# TODO
# remove csrf_exempt
# after testing is done
urlpatterns = [
    path('client/<int:client_id>/case', ClientCaseView.as_view()),
    path('case', CaseView.as_view()),
    path('case/<int:case_id>/contact', ContactView.as_view()),
    path('case/<int:case_id>/document', CaseDocumentsView.as_view()),
    path('case/<int:case_id>/document/<int:document_id>',
         DownloadDocumentView.as_view()),
    path('case/<int:case_id>/timeline', TimeLineEntryView.as_view()),
    path('case/<int:case_id>/timeline/<int:timeline_id>',
         TimelineSingleEntryView.as_view()),
]
