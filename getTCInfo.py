import ROOT
import math

def plot(hist,name):

    c1 = ROOT.TCanvas()
    hist.GetXaxis().SetTitle("#eta")
    hist.GetYaxis().SetTitle("#phi")
    hist.Draw("COLZ")
    c1.Draw()
    c1.SaveAs(name+".pdf")



def main():

    tfile = ROOT.TFile.Open("ntuple.root")
    ttree = tfile.Get("hgcalTriggerNtuplizer/HGCalTriggerNtuple")

    nevents = 100
    energyweighted = True
    makeplots = False
    maketxt = True

    if maketxt:
        out = open("info.csv", "w")

    
    for i,event in enumerate(ttree):
        out.write("event number " + str(i) + " positive end-cap\n")
        if ( i == nevents ):
            break
        h1p = ROOT.TH2D("tc_positive"+str(i),"TCs Event" + str(i) + " +z", 50, 1.0, 3.5, 50, -math.pi, math.pi)
        h1n = ROOT.TH2D("tc_negative"+str(i),"TCs Event" + str(i) + " +z", 50, 1.0, 3.5, 50, -math.pi, math.pi)
        h2p = ROOT.TH2D("gen_positive"+str(i),"Gen Particles Event" + str(i) + " +z", 50, 1.0, 3.5, 50, -math.pi, math.pi)
        h2n = ROOT.TH2D("gen_negative"+str(i),"Gen Particles Event" + str(i) + " +z", 50, 1.0, 3.5, 50, -math.pi, math.pi)

        #TCs
        out.write("trigger cells r/z, phi, energy_t, layer\n")
        for eta,phi,energy,pt,x,y,z,layer in zip(event.tc_eta, event.tc_phi, event.tc_energy, event.tc_pt, event.tc_x, event.tc_y, event.tc_z, event.tc_layer):
            if ( eta<0 ):
                continue
            if energyweighted:
                h1p.Fill(abs(eta),phi,energy)
            else:
                h1p.Fill(abs(eta),phi)

            if maketxt:
                r = math.sqrt(x*x + y*y)
                roverz = abs(r/z)
                out.write(str(roverz) + ", " + str(phi) + ", " + str(pt) + "\n")
        #Gen
        out.write("stable gen particles eta, phi, energy_t, pdgid\n")
        for pdgid,eta,phi,energy,status in zip(event.gen_pdgid, event.gen_eta, event.gen_phi, event.gen_energy, event.gen_status):

            if ( status != 1 ):
                continue
            if ( eta<0 ):
                continue
            if energyweighted:
                h2p.Fill(abs(eta),phi,energy)
            else:
                h2p.Fill(abs(eta),phi)
            et = energy/math.cosh(eta)

            if maketxt:
                out.write (str(eta) + ", " + str(phi) + ", " + str(et) + ", " + str(pdgid) + "\n")

        out.write ("event number " + str(i) +  " negative end-cap\n")

        #TCs
        out.write ("trigger cells r/z, phi, energy_t, layer\n")
        for eta,phi,energy,pt,x,y,z,layer in zip(event.tc_eta, event.tc_phi, event.tc_energy, event.tc_pt, event.tc_x, event.tc_y, event.tc_z, event.tc_layer):
            if ( eta>=0 ):
                continue
            if energyweighted:
                h1n.Fill(abs(eta),phi,energy)
            else:
                h1n.Fill(abs(eta),phi)

            if maketxt:
                r = math.sqrt(x*x + y*y)
                roverz = abs(r/z)
                out.write(str(roverz) + ", " + str(phi) + ", " + str(pt) + + ", " + str(layer) + "\n")

        #Gen
        out.write ("stable gen particles eta, phi, energy_t, pdgid\n")
        for pdgid,eta,phi,energy,status in zip(event.gen_pdgid, event.gen_eta, event.gen_phi, event.gen_energy, event.gen_status):

            if ( status != 1 ):
                continue
            if ( eta>=0 ):
                continue
            if energyweighted:
                h2n.Fill(abs(eta),phi,energy)
            else:
                h2n.Fill(abs(eta),phi)
            et = energy/math.cosh(eta)

            if maketxt:                
                out.write (str(eta) + ", " + str(phi) + ", " + str(et) + ", " + str(pdgid) + "\n")

        if makeplots:
            plot(h1p,h1p.GetName())
            plot(h1n,h1n.GetName())
            plot(h2p,h2p.GetName())
            plot(h2n,h2n.GetName())

main()    
