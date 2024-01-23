const fs=require('fs')
const styles=JSON.parse(fs.readFileSync('styles.json'));
const cats=JSON.parse(fs.readFileSync('categories.json'));

console.log(Object.keys(cats).map(c=>{return cats[c].map(s=>s=styles[s] || cats[s]? undefined : s).filter(Boolean)}).filter(e=>e.length).join('\n'))
