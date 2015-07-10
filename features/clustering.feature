Feature: Couchbase clustering

  Scenario: Rebalance one node out with the travel sample loaded
    Given we have 4 nodes running
     When we initialized a single node on "127.0.0.1:9000"
      Then we add node "127.0.0.1:9001" to the cluster
      And we add node "127.0.0.1:9002" to the cluster
      And we add node "127.0.0.1:9003" to the cluster
      And we rebalance the cluster
      And we load the "travel-sample" dataset
      And we remove node "127.0.0.1:9002" from the cluster
