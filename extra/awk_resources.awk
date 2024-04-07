BEGIN {
    print ".PHONY : get-resources\n"
}
/.*\.tsp/ {
    target = target " ./resources/"$0 ;
    print "./resources/"$0": \n\twget http://comopt.ifi.uni-heidelberg.de/software/TSPLIB95/tsp/"$0".gz -O ./resources/"$0".gz\n\tgunzip ./resources/"$0".gz\n" 
}
/.*\.atsp/ {
    target = target " ./resources/"$0 ;
    print "./resources/"$0": \n\twget http://comopt.ifi.uni-heidelberg.de/software/TSPLIB95/atsp/"$0".gz -O ./resources/"$0".gz\n\tgunzip ./resources/"$0".gz\n" 
}
END {
    print "get-resources:"target
}