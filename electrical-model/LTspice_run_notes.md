# LTspice Operating-Point Run Notes

The committed schematic `BUCK_converter.asc` preserves the **10 A baseline** configuration.

The 5 A, 10 A and 20 A LTspice loss values were obtained from the **same circuit topology and component settings** by changing only the resistive load to set the desired nominal output current at 12 V:

| Nominal load current | Load resistance | Recorded LTspice MOSFET average loss |
|---:|---:|---:|
| 5 A | 2.4 Ω | 0.221 W |
| 10 A | 1.2 Ω | 0.731 W |
| 20 A | 0.6 Ω | 2.744 W |

Separate `.asc` copies were not retained for the 5 A and 20 A runs; the user changed the load resistance in the same schematic and recorded the results. The committed `.asc` therefore acts as the reproducible baseline circuit definition, while this file records the operating-point changes used for the two additional LTspice runs.

For the 10 A validation case, the exported steady-state VDS/ID waveform in `notebook/Exported_vds_Id_steady_state.txt` is used for direct power integration and conduction/switching decomposition.
