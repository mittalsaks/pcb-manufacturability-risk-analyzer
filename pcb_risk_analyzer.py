import pcbnew

from .copper_density import analyze_copper_density, interpret_density


class PCBRiskAnalyzerPlugin(pcbnew.ActionPlugin):

    def defaults(self):
        self.name = "PCB Manufacturability Risk Analyzer"
        self.category = "Manufacturing Analysis"
        self.description = "Detect fabrication risks before PCB manufacturing"

    def Run(self):

        board = pcbnew.GetBoard()

        print("\n=== PCB Manufacturability Analysis ===\n")

        # ---------------------------
        # Phase 1 : Trace Analysis
        # ---------------------------

        tracks = board.GetTracks()

        total_width = 0
        track_count = 0

        for item in tracks:

            if isinstance(item, pcbnew.PCB_TRACK):

                total_width += item.GetWidth()
                track_count += 1

        if track_count > 0:
            avg_width = total_width / track_count
        else:
            avg_width = 0

        print("Average Trace Width:", avg_width)

        # Basic trace risk estimation
        if avg_width < 150000:
            print("Trace Risk Level: HIGH (very thin traces)")
        elif avg_width < 300000:
            print("Trace Risk Level: MODERATE")
        else:
            print("Trace Risk Level: LOW")

        print("\n-----------------------------------\n")

        # ---------------------------
        # Phase 2 : Copper Density
        # ---------------------------

        grid, imbalance = analyze_copper_density(board)

        print("Copper Density Imbalance:", imbalance)

        status = interpret_density(imbalance)

        print("Copper Distribution:", status)

        print("\n-----------------------------------\n")

        # ---------------------------
        # Overall Manufacturing Risk
        # ---------------------------

        if imbalance > 0.4:
            overall = "HIGH"
        elif imbalance > 0.2:
            overall = "MODERATE"
        else:
            overall = "LOW"

        print("Manufacturing Risk:", overall)

        print("\n=== Analysis Complete ===\n")


PCBRiskAnalyzerPlugin().register()
