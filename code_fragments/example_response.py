#%% Add to sys path
import TEM_tools as te
from campaign_20240522.filtering_20240522 import root_path

#%%

if __name__ is '__main__':
    folder_handler = te.core.FolderHandler(root_path / 'data/20240522', 'tem_default', save_log=False)
    target_dir = folder_handler.folder_structure.get('data_forward')

    # Preprocessing
    modeller = te.tem.ForwardTEM()

    # Set loop size in meters (side length of the square loop)
    modeller.loop = 15

    # Choose the current key: 1 or 4 (A)
    modeller.currentkey = 4

    # Choose time key: 1 - 9 (number of timegates)
    modeller.timekey = 4

    # Add a title to the plot
    modeller.plot_title = 'Example Response'

    # Thickness of each layer in meters
    thks = [5, 10, 5]

    # Resistivity of each layer in Ohm meters
    rho = [30, 10, 30]

    # Add the model with the thickness and resistivity of each layer
    modeller.add_resistivity_model(thickness=thks, resistivity=rho)

    # Run the forward modeller
    modeller.run()

    # Save the figure
    modeller.savefig(target_dir / 'example_response.png')

