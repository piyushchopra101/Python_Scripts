# Final Project Work for Analytics in Python.
# Creating classes and  learning object oriented programming

import random
import math

###############################################################
# max_offer - the maximal amount the funder is willing to provide for project completion (float)
# final_offer - the contracted amount, which the winning bidder receives (float)
# cost - the cost of executing the project (float)
# winning_bidder_index - the index of the bidder (if any) that wins the RFT (integer)
# NOTE: the profit that a winning bidder (if any) will secure is "final_offer - cost"
class RFT( object ):

    # RFT object initializer
    # ARGUMENTS: xavg_offer (the mean of Exponential distribution, from which max_offer will be generated)
    # RETURNS: an RFT object
    def __init__( self, xavg_offer ):
        self.max_offer = random.expovariate( 1.0 / xavg_offer )
        self.cost = 100000.0       
        self.final_offer = None
        self.winning_bidder_index = None
 
    # This method updates (if needed) the final_offer amount for which the RFT is contracted and the index of the winning bidder, when the word from the action has been received
    # ARGUMENTS: xoffer (the contracted amount), xindex (the index of the winning bidder) 
    # RETURNS: VOID       
    def ProcessAuctionOutcome( self, xoffer, xindex ):
        self.final_offer = xoffer
        self.winning_bidder_index = xindex
        print 'The index of the winning bidder is', xindex, 'offering', xoffer, 'dollars' 


###################################################################
# index - the index assigned to the bidder at its creation (integer)
# secured_rfts - a list of RFT objects that the bidder won over all of the auctions
# earnings - total earnings attained by the bidder up to the current period (float)
# history - a list of records about the auction outcome history (to be used at bidder’s discretion)
class Bidder( object ):
    
    # Bidder object initializer
    # ARGUMENTS: xindex (the index that the Auction assigns to the bidder when adding it), xearnings (set equal to 0.0 by default)
    # RETURNS: a Bidder object
    def __init__( self, xindex, xearnings = 0.0 ):
        self.index = xindex
        self.history = []
        self.earnings = xearnings
        self.secured_rfts = []
        
    # This method determines what the bidder would like to bid for the current RFT 
    # ARGUMENTS: xrft (the RFT available to bid on) 
    # RETURNS: float
    def Bid( self, xrft ):
        maximal_potential_profit = xrft.max_offer - xrft.cost
        random_number = random.random()
        if random_number < 0.2 or maximal_potential_profit <= 0.0:
            print 'Bidder', self.index, 'chooses not to bid'            
            return 0.0
        else:
            my_bid = xrft.cost + random.uniform( 0, maximal_potential_profit )
            print 'Bidder', self.index, 'bids', my_bid              
            return my_bid

    # This method checks/updates the history list and does computations (if any) that may affect the bidding strategy in the new quarter, at its beginning
    # ARGUMENTS: None
    # RETURNS: VOID   
    def PrepareForAuction( self ):
        self.history = []
            
    # This method updates the history after the auction outcomes on an RFT has been announced, and if the bidder has won it, updates the earnings and the list of secured RFTs
    # ARGUMENTS: xrft - the RFT, for which the bidding has just completed
    # RETURNS: VOID           
    def ProcessAuctionOutcome( self, xrft ):
        if xrft.winning_bidder_index == self.index:
            self.secured_rfts.append( xrft )
            self.earnings = self.earnings + xrft.final_offer - xrft.cost
            print 'My earnings are now', self.earnings
        self.history.append( ( xrft.max_offer, xrft.final_offer ) )  


###########################################################################        
# bidders – a list of Bidder objects eligible to participate in RFT bidding
# rfts - a list of all RFT objects maintained and updated as new RFTs arrive
# total_quarters - number of quarters for which the simulation will run (integer)
# avg_rfts - average number of RFTs to become available in a quarter (integer) [the distribution of the number of RFTs in a quarter is assumed Geometric]
# avg_offer - average amount (in dollars) that a funder offers for completing their project (float) [the distribution of this amount is assumed Exponential]
# bids - a list of floats, the bids from for the current RFT (the size of the list is equal to the size of the bidders list) 
# quarter - current simulation quarter (integer)
class Auction( object ):
    
    # Auction object initializer
    # ARGUMENTS: number of quarters in the simulation run, average number of RFTs per quarter (set it to 15), average amount offered per RFT (set it to 120000.0)
    # RETURNS: an Auction object
    def __init__( self, xquarters, xavg_rfts = 15, xavg_offer = 120000.0 ):
        self.bidders = []
        self.rfts = []       
        self.total_quarters = xquarters
        self.avg_rfts = xavg_rfts
        self.avg_offer = xavg_offer
        self.quarter = 0
        self.bids = []
        self.bidder_securedrfts = []
        self.bidder_profits = []
        print 'The simulation is set up for', self.total_quarters, 'quarters' 
              
    # This method adds a new Bidder object to the list of bidders, and updates the size of the lists of (1) bids and (2) RFT counts secured by bidders (in current quarter) and (3) bidder profits
    # ARGUMENTS: a Seller object to be added
    # RETURNS: VOID
    def AddBidder( self, xbidder ):
        self.bidders.append( xbidder )
        self.bids.append( 0 )
        self.bidder_securedrfts.append( 0 )
        self.bidder_profits.append( 0 )
 
    # This method asks bidders to bid for an RFT and stores the submitted bids; if a bidder has already secured two projects in a quarter, their bid is disregarded not to overload them in this quarter
    # ARGUMENTS: xrft - the RFT for which bids are requested
    # RETURNS: VOID
    def SolicitBids( self, xrft ):
        for i in range( 0, len(self.bidders) ):
            self.bids[ i ] = self.bidders[ i ].Bid( xrft )
            if self.bidder_securedrfts[ i ] == 2:
                self.bids[ i ] = 0

    # This method determines the winner (if any) for an RFT, based on the lowest bid (in a case of a tie, the winner is selected randomly); then, lets the RFT and the bidders process this news  
    # ARGUMENTS: xrft - the RFT for which bids have been requested
    # RETURNS: VOID
    def AnnounceWinner( self, xrft ):
        winning_bid = xrft.max_offer
        winning_bidder_indices = []
        for i in range( 0, len(self.bidders) ):
            if self.bids[ i ] > 0 and self.bids[ i ] <= winning_bid:
                if len( winning_bidder_indices ) == 0 or self.bids[ i ] == winning_bid:
                     winning_bid = self.bids[ i ]
                     winning_bidder_indices.append( i )
                else:
                    winning_bid = self.bids[ i ]
                    winning_bidder_indices = [ i ]
        if len( winning_bidder_indices ) > 0:
            winner_index = random.choice( winning_bidder_indices )
            self.bidder_securedrfts[ winner_index ] = self.bidder_securedrfts[ winner_index ] + 1
            xrft.ProcessAuctionOutcome( winning_bid, winner_index )
        for i in range( 0, len(self.bidders) ):
            self.bidders[ i ].ProcessAuctionOutcome( xrft )
    
    # This method lets the bidders update their records (if they desire) in anticipation of an auction in an upcoming quarter
    # ARGUMENTS: none
    # RETURNS: VOID
    def AnnounceAuction( self ):
        for i in range( 0, len(self.bidder_securedrfts) ):
            self.bidder_securedrfts[ i ] = 0
        for b in self.bidders:
            b.PrepareForAuction()
    
    # This method generates RFTs as they arrive in a quarter, and for each arriving RFT, stores it and runs an auction for it, i.e., solicits bids and announces winners
    # ARGUMENTS: none
    # RETURNS: VOID
    def SimulateAuction( self ):
        while random.random() > 1.0/self.avg_rfts:
            new_rft = RFT( self.avg_offer )
            self.rfts.append( new_rft )
            print 'It is Quarter #', self.quarter, '. RFT #', len( self.rfts ), 'has become available. The maximal offer is', new_rft.max_offer
            self.SolicitBids( new_rft )
            self.AnnounceWinner( new_rft )
            
    # This method runs the simulation for the pre-set number of quarters using the methods above, and at the end, prints out the the bidders’ achieved earnings
    # ARGUMENTS: none
    # RETURNS: VOID
    def Run( self ):
        for i in range( 1, self.total_quarters + 1 ):
            self.quarter = self.quarter + 1
            self.AnnounceAuction()
            self.SimulateAuction()
            for b in self.bidders:
                print 'The earnings of Bidder', b.index, 'amount to', b.earnings, 'dollars'



class Bidder1( Bidder ):
    
    # Bidder object initializer
    # ARGUMENTS: xindex (the index that the Auction assigns to the bidder when adding it), xearnings (set equal to 0.0 by default)
    # RETURNS: a Bidder object
    def __init__( self, xindex,  xearnings = 0.0 ):
        self.index= xindex
        self.secured_rfts= []
        self.earnings= xearnings 
        self.history=[]
        self.others_wins= [0]*5
        self.num_eliminated= 0
        

        
        
    # This method determines what the bidder would like to bid for the current RFT 
    # ARGUMENTS: xrft (the RFT available to bid on) 
    # RETURNS: float
    def Bid( self, xrft ):
        offer=0
        # if Max offer generated is greater than cost and we have not secured any 
        # RFT then we have the following less risky strategy based on the the 
        # number of bidders participating in the auction (having not secured 2 rfts)
        if  xrft.max_offer>xrft.cost: 
            if len(self.secured_rfts)==0:
                if self.num_eliminated ==4 :
                    offer = xrft.max_offer
                elif self.num_eliminated > 3:    
                    offer= xrft.cost + 0.49*(xrft.max_offer - xrft.cost)
                elif self.num_eliminated > 2 :
                    offer= xrft.cost + 0.49*(xrft.max_offer - xrft.cost)
                elif self.num_eliminated > 1 :
                    offer= xrft.cost + 0.49*(xrft.max_offer - xrft.cost)
                else:
                    offer = xrft.cost + 0.49*(xrft.max_offer - xrft.cost)
        # if Max offer generated is greater than cost and we have secured one  
        # RFT then we have the following more  risky strategy based on the the 
        # number of bidders participating in the auction (having not secured 2 rfts)
            if len(self.secured_rfts)==1:
                if self.num_eliminated ==4 :
                    offer = xrft.max_offer
                elif self.num_eliminated > 3:    
                    offer= xrft.cost + 0.49*(xrft.max_offer - xrft.cost)
                elif self.num_eliminated>2 :
                    offer= xrft.cost + 0.49*(xrft.max_offer - xrft.cost)
                elif self.num_eliminated > 1:
                    offer= xrft.cost + 0.49*(xrft.max_offer - xrft.cost)
                else:
                    offer = xrft.cost + 0.49*(xrft.max_offer - xrft.cost)
                    
        # if Max offer generated is less than cost we will give an unreasonably high
        # bid to not partcipate and avoid loss             
        else : 
            offer = 1000*xrft.max_offer
        
        return offer
        


    # This method checks/updates the history list and does computations (if any) that may affect the bidding strategy in the new quarter, at its beginning
    # ARGUMENTS: None
    # RETURNS: VOID   
    def PrepareForAuction( self ):
    # the following code calculates the number of bidders who alredy secured 2 bids
       if len(self.history)>0 and self.history[-1].winning_bidder_index != None  :     
           a=self.history[-1].winning_bidder_index

           self.others_wins[a]= self.others_wins[a]+1
           self.num_eliminated= len([i for i in self.others_wins if i== 2])


            
    # This method updates the history after the auction outcomes on an RFT has been announced, and if the bidder has won it, updates the earnings and the list of secured RFTs
    # ARGUMENTS: xrft - the RFT, for which the bidding has just completed
    # RETURNS: VOID           
    def ProcessAuctionOutcome( self, xrft ):
        self.history.append(xrft)
        if self.index== xrft.winning_bidder_index :
            self.earnings= self.earnings + xrft.final_offer -xrft.cost
            self.secured_rfts.append(xrft)
            


############################################################           
# THE MAIN CODE THAT EXECUTES THE SIMULATION
# This code creates an Auction object with a given number of quarters to run, creates and adds bidders, and lets the Auction run
anAuction = Auction( 2000 )
anAuction.AddBidder( Bidder( 0 ) )
print 'Bidder 0 has been added.'
anAuction.AddBidder( Bidder1( 1 ) )
print 'Bidder 1 has been added.'
anAuction.AddBidder( Bidder( 2 ) )
print 'Bidder 2 has been added.'
anAuction.AddBidder( Bidder( 3 ) )
print 'Bidder 3 has been added.'
anAuction.AddBidder( Bidder( 4 ) )
print 'Bidder 4 has been added.'
anAuction.Run()











