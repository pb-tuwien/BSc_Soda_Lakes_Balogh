#%% Add to sys path
import TEM_tools as te
from campaign_20240522.filtering_20240522 import root_path

if __name__ == '__main__':
    target_dir = root_path / 'data' / 'example_modelled'
    target_dir.mkdir(parents=True, exist_ok=True)

    # Preprocessing
    modeller = te.tem.ForwardTEM()

    # Set loop size in meters (side length of the square loop)
    modeller.loop = 15

    # Choose the current key: 1 or 4 (A)
    modeller.currentkey = 4

    # Choose time key: 1 - 9 (number of timegates)
    modeller.timekey = 6

    # Add a title to the plot
    modeller.plot_title = 'Example Response'

    # Thickness of each layer in meters
    thks = [30, 10, 30]

    # Resistivity of each layer in Ohm meters
    rho = [30, 20, 30]

    # Add the model with the thickness and resistivity of each layer
    modeller.add_resistivity_model(thickness=thks, resistivity=rho)

    # Run the forward modeller
    modeller.run()

    # Save the figure
    modeller.savefig(target_dir / 'example_response.png')

