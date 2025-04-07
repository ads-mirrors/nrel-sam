import sco2_baseline_sim_eta8085
import sco2_baseline_sim_eta8090

if __name__ == "__main__":
    
    # Run both efficiency cases
    sco2_baseline_sim_eta8090.run_G3P3_sweeps(10)
    sco2_baseline_sim_eta8085.run_G3P3_sweeps(10)