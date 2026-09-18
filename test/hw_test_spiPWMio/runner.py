from ttboard.demoboard import DemoBoard
from ttboard.mode import RPMode
# from microcotb as cocotb

def main():
    # import ttboard.cocotb.dut

    tt = DemoBoard.get()

    # check if chip has the targt project
    if not tt.shuttle.has('tt_um_fhw_appel_spiPWMio'):
        print("The shuttle doesn't have tt_um_fhw_appel_spiPWMio!")
        return

    # Wrapper for reuse Pin naming

    # Setup Design
    tt.shuttle.tt_um_fhw_appel_spiPWMio.enable()

    # Initial Tests

    # Cocotb tests

    return 