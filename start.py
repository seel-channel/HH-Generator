from HH import HH

if __name__ == '__main__':
    #USING SPLITTED DATA
    high = "./data/MSEED/20/"
    low = "./data/MSEED/0/"
    HH( [high+"9CG.e.mseed", high+"9CG.n.mseed", high+"9CG.z.mseed"],
        [low+"R1235.CG.e.mseed", low+"R1235.CG.n.mseed", low+"R1235.CG.z.mseed"])

    #USING MERGED DATA
    file = "./data/ASCII merge/SNRA9510.091"
    HH( [file], None,
        start_whole=[0,0],
        end_whole=[0,0],
        use_baseline_correction=False)
    
    #USING DISORDENED DATA PATHS
    HH( [high+"9CG.z.mseed", high+"9CG.e.mseed", high+"9CG.n.mseed"],
        [low+"R1235.CG.e.mseed", low+"R1235.CG.z.mseed", low+"R1235.CG.n.mseed"],
        channel_order = [["Z", "EW", "NS"], ["EW", "Z", "NS"]])