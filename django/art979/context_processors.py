from art979.Art.forms import CreateSongForm, CreateAlbumForm, CreateVisualPieceForm, CreateLiteraturePieceForm, CreatePerformingPieceForm, CreateFoodForm, CreateFilmForm

def site_forms(request):
    """
    Template variables for forms
    """

    context = {}
    context['songform'] = CreateSongForm()
    context['albumform'] = CreateAlbumForm()

    return context
