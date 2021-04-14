import ROOT
import math

def plot(hist,name):

    c1 = ROOT.TCanvas()
    hist.GetXaxis().SetTitle("#eta")
    hist.GetYaxis().SetTitle("#phi")
    hist.Draw("COLZ")
    c1.Draw()
    c1.SaveAs(name+".pdf")





tfile = ROOT.TFile.Open("ntuple.root")
ttree = tfile.Get("hgcalTriggerNtuplizer/HGCalTriggerNtuple")

#outroot = ROOT.TFile.Open("hist.root", "RECREATE")

for i,event in enumerate(ttree):
    print ("event number ", i, " positive end-cap")
    # if ( i > 2 ):
    #     break
    h1p = ROOT.TH2D("tc_positive"+str(i),"TCs Event" + str(i) + " +z", 50, 1.0, 3.5, 50, -math.pi, math.pi)
    h1n = ROOT.TH2D("tc_negative"+str(i),"TCs Event" + str(i) + " +z", 50, 1.0, 3.5, 50, -math.pi, math.pi)
    h2p = ROOT.TH2D("gen_positive"+str(i),"Gen Particles Event" + str(i) + " +z", 50, 1.0, 3.5, 50, -math.pi, math.pi)
    h2n = ROOT.TH2D("gen_negative"+str(i),"Gen Particles Event" + str(i) + " +z", 50, 1.0, 3.5, 50, -math.pi, math.pi)
    
    #TCs
    print ("trigger cells eta,phi,energy_t")
    for eta,phi,energy,pt in zip(event.tc_eta, event.tc_phi, event.tc_energy, event.tc_pt):
        if ( eta<0 ):
            continue
        h1p.Fill(abs(eta),phi)
        #print (str(eta) + "," + str(phi) + "," + str(pt))
    #Gen
    print ("stable gen particles eta,phi,energy_t,pdgid")
    for pdgid,eta,phi,energy,status in zip(event.gen_pdgid, event.gen_eta, event.gen_phi, event.gen_energy, event.gen_status):

        if ( status != 1 ):
            continue
        if ( eta<0 ):
            continue
        h2p.Fill(abs(eta),phi)
        et = energy/math.cosh(eta)
        #print (str(eta) + "," + str(phi) + "," + str(et) + "," + str(pdgid))

    print ("event number ", i, " negative end-cap")

    #TCs
    print ("trigger cells eta,phi,energy_t")
    for eta,phi,energy,pt in zip(event.tc_eta, event.tc_phi, event.tc_energy, event.tc_pt):
        if ( eta>=0 ):
            continue
        #print (str(abs(eta)) + "," + str(phi) + "," + str(pt))
        h1n.Fill(abs(eta),phi)
        
    #Gen
    print ("stable gen particles eta,phi,energy_t,pdgid")
    for pdgid,eta,phi,energy,status in zip(event.gen_pdgid, event.gen_eta, event.gen_phi, event.gen_energy, event.gen_status):

        if ( status != 1 ):
            continue
        if ( eta>=0 ):
            continue
        et = energy/math.cosh(eta)
        #print (str(eta) + "," + str(phi) + "," + str(et) + "," + str(pdgid))
        #h2n.Fill(abs(eta),phi,energy)
        h2n.Fill(abs(eta),phi)

    plot(h1p,h1p.GetName())
    plot(h1n,h1n.GetName())
    plot(h2p,h2p.GetName())
    plot(h2n,h2n.GetName())
    
#     h1p.Write()
#     h1n.Write()
#     h2p.Write()
#     h2n.Write()


# outroot.Close()
