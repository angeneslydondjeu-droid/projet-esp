from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)
donnees = {}

PAGE = """
<html><head><meta name="viewport" content="width=device-width">
<title>Tableau de bord ESP</title></head>
<body style="font-family:sans-serif;padding:20px">
<h2>Tableau de bord ESP</h2>
<div id="box">En attente de données...</div>
<script>
async function maj(){
  const r = await fetch('/api/data');
  const d = await r.json();
  let h = '';
  for (const nom in d){
    const e = d[nom];
    h += '<h3>' + nom + '</h3>'
      + 'Température : ' + e.temperature + ' °C<br>'
      + 'Humidité : ' + e.humidite + ' %<br>'
      + 'Son : ' + e.son + '<br>';
  }
  if (h) document.getElementById('box').innerHTML = h;
}
setInterval(maj, 2000); maj();
</script></body></html>
"""

@app.route("/")
def accueil():
    return render_template_string(PAGE)

@app.route("/api/data", methods=["POST"])
def recevoir():
    j = request.get_json(force=True)
    donnees[j.get("esp", "esp")] = j
    return jsonify(ok=True)

@app.route("/api/data", methods=["GET"])
def lire():
    return jsonify(donnees)
