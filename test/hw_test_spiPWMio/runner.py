import gc
from ttboard.demoboard import DemoBoard
from ttboard.mode import RPMode
import microcotb as cocotb
from microcotb.clock import Clock
from microcotb.triggers import RisingEdge, FallingEdge, Timer, ClockCycles
from microcotb.time.value import TimeValue
from microcotb.utils import get_sim_time
gc.collect()

cocotb.set_runner_scope(__name__)

async def initialize_dut(dut):
    """Initialize the DUT"""
    clock = Clock(dut.clk, 83, units="ns")
    cocotb.start_soon(clock.start())
    dut.ena.value = 1
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 10)
    dut.rst_n.value = 1
    await ClockCycles(dut.clk, 1)


@cocotb.test()
async def smoke_test_spiPWMio(dut):
    """Smoke test for the spiPWMio project"""
    dut._log.info("Smoke test was successful")

@cocotb.test()
async def reset_test(dut):
    """Reset test for the spiPWMio project"""
    await initialize_dut(dut)
    dut._log.info("Reset test was successful")


def main():
    import ttboard.cocotb.dut

    tt = DemoBoard.get()

    # check if chip has the targt project
    if not tt.shuttle.has('tt_um_fhw_appel_spiPWMio'):
        print("The shuttle doesn't have tt_um_fhw_appel_spiPWMio!")
        return
    print("The shuttle Project tt_um_fhw_appel_spiPWMio is available.")

    # Wrapper for reuse Pin naming
    class DUT(ttboard.cocotb.dut.DUT):
        def __init__(self):
            super().__init__('spiPWMio testbench')
            self.tt = DemoBoard.get()
            # inputs
            self.add_bit_attribute('pwm_in', self.tt.ui_in, 7)
            self.add_slice_attribute('ipins', self.tt.ui_in, 6, 0)
            self.add_bit_attribute('spi_sck', self.tt.uio_in, 7)
            self.add_bit_attribute('spi_mosi', self.tt.uio_in, 5)
            self.add_bit_attribute('spi_cs_n', self.tt.uio_in, 4)                        
            # outputs
            self.add_bit_attribute('pwm_sig', self.tt.uo_out, 7)
            self.add_slice_attribute('opins', self.tt.uo_out, 6, 0)
            self.add_bit_attribute('spi_miso', self.tt.uio_in, 6)                        
                        
                        
    # Setup Design
    tt.shuttle.tt_um_fhw_appel_spiPWMio.enable()
    print("Project tt_um_fhw_appel_spiPWMio enabled")
    tt.clock_project_PWM(12e6)
    print("Clock has been set to 12 MHz")

    # Change RPMode
    if tt.mode != RPMode.ASIC_RP_CONTROL:
        print("Changing RPMode to ASIC_RP_CONTROL")
        tt.mode = RPMode.ASIC_RP_CONTROL

    # Set bidirectional pins
    tt.uio_oe_pico.value = 0b10110000
    # spi_sck, spi_mosi, spi_cs_n are driven by the RP, spi_miso is driven by the DUT

    TimeValue.ReBaseStringUnits = True


    runner = cocotb.get_runner(__name__)

    dut = DUT()
    dut._log.info(f"Enabled spiPWMio project. Will test with {runner}")

    runner.test(dut)

    dut._log.info("Test finished")

    return 


