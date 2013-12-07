/* 
 
 A few functions for encoding a selection as a short, USL-friendly string.
 This can be used with history.js to update the URL based on the current selection and eventually decode it and display the relevant selection.
 
 NB MS won't like "const"
 
*/
 
 
    // To allow us to work with large integers,
    // we use an array of smaller integers, representing parts of the bits
    // This number is the number of bits per item
    const BITS_PER_ITEM = 30;
 
    // The URL-friendly alphabet used for base64 encoding
    // Using dot for zero, making "/./" and "/../" impossible
    const ALPHABET = '.123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz-0';
    const BLOCK_LENGTH = ALPHABET.length.toString(2).length - 1;
 
    function encode(selection) {
        // Encode the currently selected filters into an integer
        var val = selection_to_integer(selection);
 
        // Compress and return as a base36 string
        return base64_encode(compress_sparse_binary(val));
    }
 
    function base64_encode(bin) { 
        var output = [];
 
        // Make sure we have blocks of six
        var padding = bin.length % BLOCK_LENGTH;
        if (padding > 0) {
            bin = Array(BLOCK_LENGTH+1-padding).join("0") + bin;
        }
 
        // Convert each block of six to a character
        for (var i=0; i < bin.length; i+=BLOCK_LENGTH) { 
            output.push(ALPHABET[parseInt(bin.slice(i, i+BLOCK_LENGTH),2)]);
        }
 
        return output.join("");
    }
 
    function selection_to_integer(selection) {
        // Remove invalid and duplicates
        var max_val = 0;
        var clean_selection = {};
        for (var i in selection) {
            var ival = selection[i];
            if (ival > 0) 
                clean_selection[ival] = true;
                max_val = ival > max_val ? ival : max_val;
        }
        // To avoid problems with javascript's number storage, we divide the bits
        // into an array. Each item has BITS_PER_ITEM bits.
 
        // Prepare result array
        var result = Array(Math.floor((max_val-1) / BITS_PER_ITEM) + 1);
        for (var i=0;i<result.length;i++) result[i] = 0;
 
        var val = 0;
        for (i in clean_selection) {
            var set = Math.floor((i-1) / BITS_PER_ITEM) + 1;
            var pos = ((i-1) % BITS_PER_ITEM);
            result[result.length-set] += (1 << pos);
        }
        return result;
    }
 
 
    const SEQUENCES_OF_ZERO = [
        [36, "00"],
        [6, "10"],
        [1, "01"],
    ];
 
    function compress_sparse_binary(val) {
        // Return an integer representing the given integer in a compressed format.
        // TODO work with bit operations instead of strings
        for (var i=0; i<val.length; i++) 
            if (i == 0) {
                val[i] = val[i].toString(2);
            } else {
                var item = (val[i] + (1 << BITS_PER_ITEM)).toString(2);
                val[i] = item.slice(1);
            }
        val = val.join("").split("");
 
        // Compress the result
        var output = [];
        while (val.length > 0) {
            var next_one = val.indexOf("1");
            if (next_one == -1) 
                next_one = val.length;
            // if the next "1" was here, handle it and move on
            if (next_one == 0) {
                val.shift();
                output[output.length] = "11";
                continue;
            }
            for (var i in SEQUENCES_OF_ZERO) {
                var v = SEQUENCES_OF_ZERO[i];
                var amount = v[0];
                var bits = v[1];
                while (next_one >= amount) {
                    val = val.splice(amount, val.length - amount);
                    output[output.length] = bits;
                    next_one -= amount;
                }
            }
        }
        return output.join("")
    }