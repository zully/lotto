<!doctype html>
<meta name="viewport" content="width=device-width, initial-scale=1" />
<link rel="icon" type="image/png" href="static/favicon.png" />
<title>Welcome to LottoGen v{{ version }}</title>
<body bgcolor="white">
<font color="black">
<center>
    <img src="static/wL.png" style="width:34px;height:47px;">
    <img src="static/wO.png" style="width:34px;height:47px;">
    <img src="static/wT.png" style="width:34px;height:47px;">
    <img src="static/wT.png" style="width:34px;height:47px;">
    <img src="static/wO.png" style="width:34px;height:47px;">
    <img src="static/rG.png" style="width:34px;height:47px;">
    <img src="static/rE.png" style="width:34px;height:47px;">
    <img src="static/rN.png" style="width:34px;height:47px;">
</center><br>
<table align="center">
<form method="POST">
  <tr>
    <td>
        <h3><strong><center>Game Type</strong></center></h3>
    </td>
  </tr>
  <tr>
    <td><center>
      <select name="game_type" id="_selection" style="font-size:16px;">
      % for k,v in games.items():
        <option value="{{k}}"\\
          % if selected == k:
 selected\\
          % end
>{{v}}</option>
      % end
      </select></center><br><br></td>
  </tr>
  <tr>
    <td><center><input type="image" src="static/getmynums.png" alt="Get My Numbers!"></center></td>
  </tr>
  <tr>
    <td>
      <center><br>
      % if base:
      % for num in base:
        <img src="static/w{{!num}}.png">
      % end
      % end
      % if exn:
        <img src="static/r{{!exn}}.png">
      % end
      </center>
      <br>
    </td>
  </tr>
 </table>
</form>
% import time
% if base:
% randquery = time.time()
<br>
<center><img src='static/qrcode.png?{{randquery}}'></center>
% end
</body>

