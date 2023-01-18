function smallestEquivalentString(s1: string, s2: string, baseStr: string): string {

    const list: string[][] = []
    const map = {}
    let string = ''

    for (let i = 0; i < s1.length; i++) {
        let charArrays1 = list.findIndex(arr => arr.findIndex(str => str === s1[i]) !== -1);
        let charArrays2 = list.findIndex(arr => arr.findIndex(str => str === s2[i]) !== -1);
        let charArrayIndex = 0;

        if (charArrays1 === -1) {
            charArrayIndex = charArrays2;
        } else {
            if (charArrays2 === -1) {
                charArrayIndex = charArrays1;
            } else {
                charArrayIndex = Math.min(charArrays1, charArrays2);
            }
        }

        console.log(s1[i], s2[i], charArrays1, charArrays2, charArrayIndex)

        if (charArrayIndex !== -1) {
            if ((charArrays1 !== charArrays2) && charArrays1 !== -1 && charArrays2 !== -1) {

                if (Math.min(charArrays1, charArrays2) === charArrays1) {
                    let s2Elements = list[charArrays2];
                    list.splice(charArrays2, 1);
                    list[charArrays1] = list[charArrays1].concat(s2Elements)
                } else {
                    let s1Elements = list[charArrays1];
                    list.splice(charArrays1, 1)
                    list[charArrays2] = list[charArrays2].concat(s1Elements)
                }

            } else {
                list[charArrayIndex].push(s2[i])
                list[charArrayIndex].push(s1[i])
            }

            map[s2[i]] = charArrayIndex;
            map[s1[i]] = charArrayIndex;
        } else {
            if (s1[i] !== s2[i]) list.push([s1[i], s2[i]])
            else list.push([s1[i]])

            map[s1[i]] = list.length - 1;
            map[s2[i]] = list.length - 1;
        }
    }

    for (let i = 0; i < baseStr.length; i++) {
        if (list[map[baseStr[i]]]) {
            string += list[map[baseStr[i]]].sort()[0]
        } else string += baseStr[i]
    }

    console.log(list.map(_l => _l.sort()))



    return string;
};
// let s1 = "parker", s2 = "morris", baseStr = "parser";
// let s1 = "hello", s2 = "world", baseStr = "hold";
let s1 = "cgokcgerolkgksgbhgmaaealacnsshofjinidiigbjerdnkolc";
let s2 = "rjjlkbmnprkslilqmbnlasardrossiogrcboomrbcmgmglsrsj"
let baseStr = "bxbwjlbdazfejdsaacsjgrlxqhiddwaeguxhqoupicyzfeupcn";



console.log(smallestEquivalentString(s1, s2, baseStr))