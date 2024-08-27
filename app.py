
from os import environ
from FUSION_Handlers import LayoutHandler, DownloadHandler, GirderHandler, GeneHandler
import dash_bootstrap_components as dbc
from FUSION_Prep import Prepper
from dash_extensions.enrich import DashProxy, MultiplexerTransform
from FUSION_Main import FUSION
from FUSION_Utils import load_default_slide_list

def app(*args):
    
    # Using DSA as base directory for storage and accessing files
    dsa_url = environ.get('DSA_URL')
    try:
        username = environ.get('DSA_USER', None)
        p_word = environ.get('DSA_PWORD', None)
        if not username or not p_word:
            raise ValueError('No username or password specified')
    except Exception as e:
        username = ''
        p_word = ''
        print(f'Be sure to set an initial user dummy!')

    # Initializing GirderHandler
    dataset_handler = GirderHandler(
        apiUrl=dsa_url,
        username=username,
        password=p_word
    )
    initial_user_info = dataset_handler.user_details

    # Initial collection: can be specified as a single or multiple collections which will automatically be loaded into the visualization session
    try:
        default_items = environ.get('FUSION_INITIAL_ITEMS')
        default_items = default_items.split(',')
    except:
        # Can be one or more items
        default_items = load_default_slide_list()
    
    default_item_info = [dataset_handler.get_item_info(i) for i in default_items]

    # Saving & organizing relevant id's in GirderHandler
    print('Getting initial items metadata')
    dataset_handler.set_default_slides(default_item_info)

    # Going through fusion_configs.json, adding plugins to Prepper, initializing user studies
    # Step 1: Check for presence of required plugins
    # Step 2: Pull missing ones specified in fusion_configs.json
    # Step 3: If any user studies are specified:
    #   Step 3a: Create a collection called "FUSION User Studies"
    #   Step 3b: Create a separate item for each study containing a JSON file with questions, admins, and users (with user_type, name, and responses)
    #   Step 3c: Create a new group for each user study and add users who already have accounts to that group to enable edit access to responses file
    #   Step 3d: Specify location of associated study materials (if we want to continue to host those on FUSION (PowerPoint slides, etc.))

    # Getting usability study information
    #TODO: Generalize for other types of user studies
    print(f'Getting asset items')
    assets_path = '/collection/FUSION Assets/'
    dataset_handler.get_asset_items(assets_path)

    # Getting the slide data for DSASlide()
    slide_names = [
        {'label': i['name'],'value':i['_id']}
        for i in default_item_info
    ]

    # Required for Dash layouts, themes, and icons
    external_stylesheets = [
        dbc.themes.LUX,
        dbc.themes.BOOTSTRAP,
        dbc.icons.BOOTSTRAP,
        dbc.icons.FONT_AWESOME
        ]

    # Initializing slide datasets with public collections (edge parent folders of image items) and user upload folders
    slide_dataset = dataset_handler.update_slide_datasets(initial_user_info)

    print(f'Generating layouts')
    layout_handler = LayoutHandler()
    layout_handler.gen_initial_layout(slide_names,initial_user_info,dataset_handler.default_slides, slide_dataset)
    layout_handler.gen_vis_layout(GeneHandler(),None)
    layout_handler.gen_builder_layout(dataset_handler,initial_user_info, None)
    layout_handler.gen_uploader_layout()

    download_handler = DownloadHandler(dataset_handler)

    prep_handler = Prepper(dataset_handler)
    
    print('Ready to rumble!')
    main_app = DashProxy(
        __name__,
        external_stylesheets=external_stylesheets,
        transforms = [MultiplexerTransform()]
    )
    
    # Passing main handlers to application object
    vis_app = FUSION(
        main_app,
        layout_handler,
        dataset_handler,
        download_handler,
        prep_handler
    )


if __name__=='__main__':
    #TODO: Can add path to configs here as an input argument
    app()