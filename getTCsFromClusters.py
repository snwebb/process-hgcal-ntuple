import ROOT
import math



def main():


    
    tfile = ROOT.TFile.Open("ntuple.root")
    ttree = tfile.Get("hgcalTriggerNtuplizer/HGCalTriggerNtuple")

    out = open("tcinfo.csv", "w")
    out.write("event, clusterid, tcenergy, tclayer, tcx, tcy, tcabsz, tcabseta, tcphi\n")
    for i,event in enumerate(ttree):

        print ("Event number ", i , "\n\n")
        if i > 100:
            break

        #Get TC info cached

        tc_id = list(event.tc_id)

        tc_energy = list(event.tc_energy)
        tc_layer = list(event.tc_layer)
        tc_x = list(event.tc_x)
        tc_y = list(event.tc_y)
        tc_z = list(event.tc_z)
        tc_eta = list(event.tc_eta)
        tc_phi = list(event.tc_phi)

        

        
        for cl3d,cl3did,cl3deta in zip(event.cl3d_clusters_id, event.cl3d_id, event.cl3d_eta):

            for tcid in cl3d:

                index = tc_id.index(tcid)
                tc_energy_cl = tc_energy[index]
                tc_layer_cl = tc_layer[index]
                tc_x_cl = tc_x[index]
                tc_y_cl = tc_y[index]
                tc_z_cl = abs(tc_z[index])
                tc_eta_cl = abs(tc_eta[index])
                tc_phi_cl = tc_phi[index]
                
                out.write ( str(event.event) + ", " + str(cl3did) + ", " +  str(tc_energy_cl) + ", " + str(tc_layer_cl) + ", " + str(tc_x_cl) + ", " + str(tc_y_cl) + ", " + str(tc_z_cl) + ", " + str(tc_eta_cl) + ", " + str(tc_phi_cl) + "\n")
                

    out.close()


                

        

main()
