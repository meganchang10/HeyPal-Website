{% extends "main.html" %}
{% block content %}
{% include "header.html" %}

  <div class="row divider blue">
    <div class="col-md-12"></div>
  </div>
  <div class="row banner main">
    <div class="col-md-12 padding-mini">
      <h1>HeyPal Profile</h1>

    </div>
  </div>

<!-- FLASH CODE  -->
<div class = 'flash'>
  {% with messages = get_flashed_messages() %}
    {% if messages %}
      <ul>
      {% for message in messages %}
      <li> <strong> {{ message }} </strong> </li>
      {% endfor %}
      </ul>
    {% endif %}
  {% endwith %}
</div>
<!-- FLASH CODE  -->



<!-- Here BEGINS the page specific code  -->


  <div class="row padding-top padding-bottom">
    <div class="col-md-3">
      <form name="filter_results" method='POST'>

        <label for="tags">Interests:</label><br>
        <select name="filter_results">

          <input type="checkbox" name="tag_free" value="yes" {% if current.tag_free == "yes"%}checked {% endif %}> Free<br>
          <input type="checkbox" name="tag_sporty" value="yes" {% if current.tag_sporty == "yes"%}checked {% endif %}> Sporty<br>
          <input type="checkbox" name="tag_outdoor" value="yes" {% if current.tag_outdoor == "yes"%}checked {% endif %}> Outdoors<br>
          <input type="checkbox" name="tag_special" value="yes" {% if current.tag_special == "yes"%}checked {% endif %}> Special Occasions<br>
          <input type="checkbox" name="tag_learn" value="yes" {% if current.tag_learn == "yes"%}checked {% endif %}> Better Yourself<br>
          <input type="checkbox" name="tag_date_night" value="yes" {% if current.tag_date_night == "yes"%}checked {% endif %}> Date Night<br>

        </select>

        <button type="submit">Save Changes</button>

      </form>
    </div>
  </div>

  <!-- ENDS here  -->

{% endblock %}