console.log("app");

$(document).ready(function() {


    function loadGrammar(name) {
        $("#output").html("");

        var grammar = tracery.createGrammar(grammars[name]);
        $("#grammar").html(grammar.toText());

        //Here I want to define a array to store all the unique element that it produced
        var tweet = [];

        //Here it defines how many outputs we want
        for (var i = 0; i < 30000; i++) {
            //Checking whether the new tweet has already existed on the array
            function checkTheExistedTweet(tweet, s) {
                if (tweet.indexOf(s) === -1) {
                    //restrict the length of tweet
                    if(s.length <= 140){
                        tweet.push(s);
                  }
                } else if (tweet.indexOf(s) > -1) {}
            }

            var s = grammar.flatten("#origin#");

            checkTheExistedTweet(tweet,s)
        }

      
        //output the tweet from the list
        console.log(tweet.length)
        for (var i = 0; i < tweet.length; i++) {
           //console.log(tweet[i]);           
            var div = $("<div/>", {
                class: "outputSample",
                html: tweet[i]
            });
            $("#output").append(div);
        }

    

    }

    //Here is for setting the original database
    setTimeout(function() {
        loadGrammar("tweetbot");
    },
    10);

    $('#grammarSelect').on('change',
    function() {
        loadGrammar(this.value);
    });
});