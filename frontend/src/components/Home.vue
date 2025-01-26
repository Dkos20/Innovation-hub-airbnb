<template>
  <main>
    <div class="jumbotron">
      <h1 class="display-4">The Idea</h1>
      <p class="lead">
        Do you want to know the best price for your rental accomodation?
      </p>
      <hr class="my-4" />
      <p>
        Use AirBnb Calculator to discover the best price to rent out your
        accomodation, set the perfect price with the help of Artificial
        Intelligence and stay two steps ahead of the competition.
      </p>
      <p class="lead">
        <a class="btn btn-primary btn-lg" href="#here">Calculate Now</a>
      </p>
    </div>
    <img
      name="pic1"
      height="350px"
      id="image_home"
      width="600px"
      src="../../public/exchangeHouseMoney.webp"
    />
    <fieldset name="calculator" id="here" class="element3">
      <h1 class="calc_title">Airbnb Calculator</h1>
      <br />
      <br />
      <FormKit
        type="form"
        name="calc"
        @submit="getCoordinates"
        submit-label="Calculate"
        :submit-attrs="{
          'suffix-icon': 'submit',
        }"
        #default="{ value }"
      >
        <FormKit
          type="text"
          name="address"
          id="address"
          class="input" 
          validation="required"
          label="Address"
          help="Enter the location of the rental place"
          placeholder="77 rue La Boétie, Paris, 75015"
          v-model="address"
        />
        <input v-model="longitude" type="hidden" validation-visibility="live" />
        <input v-model="latitude" type="hidden" validation-visibility="live" />
        <br />
        <FormKit
          type="number"
          name="bedrooms"
          id="bedrooms"
          class="input" 
          label="Bedrooms"
          validation="required"
          validation-visibility="live"
          help="How many bedrooms does the rental place have?"
          v-model="bedrooms"
        />
        <br />
        <FormKit
          type="number"
          name="bathrooms"
          id="bathrooms"
          class="input" 
          label="Bathrooms"
          validation="required"
          validation-visibility="live"
          help="How many bathrooms does the rental place have?"
          v-model="bathrooms"
        />
        <br />
        <FormKit
          type="select"
          name="propertyType"
          class="input" 
          id="propertyType"
          placeholder="Select a type"
          :options="[
            'Entire rental unit',
            'Private room in rental unit',
            'Entire condo',
            'Room in boutique hotel',
            'Room in hotel',
            'Entire loft',
            'Entire home',
            'Private room in condo',
            'Entire townhouse',
            'Shared room in rental unit',
          ]"
          validation="required"
          label="Property Type"
          v-model="property_type"
        />
        <br />
        <FormKit
          type="select"
          name="roomType"
          id="roomType"
          class="input" 
          placeholder="Select a type"
          :options="[
            'Entire home/apt',
            'Private room',
            'Hotel room',
            'Shared room',
          ]"
          validation="required"
          label="Room Type"
          v-model="room_type"
        />
        <br />
          <FormKit
            type="checkbox"
            name="amenities"
            id="amenities"
            placeholder="Select amenities"
            :options="[
              {
                value: 'air_conditioning',
                label: 'Air conditioning',
              },
              {
                value: 'bed_linen',
                label: 'Bed linen',
              },
              {
                value: 'tv',
                label: 'Television',
              },
              {
                value: 'coffee_machine',
                label: 'Coffee machine',
              },
              {
                value: 'cooking_basics',
                label: 'Cooking utensils',
              },
              {
                value: 'white_goods',
                label: 'White goods',
              },
              {
                value: 'elevator',
                label: 'Elevator',
              },
              {
                value: 'parking',
                label: 'Parking',
              },
              {
                value: 'host_greeting',
                label: 'Host greeting',
              },
              {
                value: 'internet',
                label: 'Internet',
              },
              {
                value: 'long_term_stays',
                label: 'Long term stays',
              },
              {
                value: 'private_entrance',
                label: 'Private entrance',
              },
              {
                value: 'other',
                label: 'Other',
              },
            ]"
            label="Amenities"
            v-model="amenities"
          />
          <br />
          <FormKit
            type="number"
            name="accomodates"
            id="accomodates"
            validation="required"
            label="Number of Accomodates"
            help="Enter the number of accomodates"
            v-model="accomodates"
          />
          <br />
          <FormKit
            type="number"
            name="minimum_nights"
            id="minimum_nights"
            validation="required"
            label="Number of Minimum nights"
            v-model="minimum_nights"
          />
          <br />
          <FormKit
            type="number"
            name="maximum_nights"
            id="maximum_nights"
            validation="required"
            label="Number of Maximum nights"
            v-model="maximum_nights"
          />
          <br />
          <div id="calculated-price">
          <FormKit
            type="text"
            name="calculation"
            id="calculation"
            label="Calculated price:"
            v-model="calculated_price"
            placeholder="€0"
            readonly
          />
        </div>
      </FormKit>
    </fieldset>
  </main>
</template>

<script>
import axios from "axios";
import { createToaster } from "@meforma/vue-toaster";
const toaster = createToaster();
toaster.show("Make an account to use the calculator!");
export default {
  name: "Home",
  data() {
    return {
      address: "",
      longitude: "",
      latitude: "",
      bedrooms: "",
      bathrooms: "",
      accomodates: "",
      room_type: "",
      property_type: "",
      amenities: "",
      minimum_nights: "",
      maximum_nights: "",
      calculated_price: 0,
    };
  },
  methods: {
    async getCoordinates() {
      this.isLoading = true;
      try {
        const response = await axios.get(
          `https://maps.googleapis.com/maps/api/geocode/json?address=${this.address}&key=YOUR_API_KEY:)`
        );
        this.longitude = response.data.results[0].geometry.location.lng;
        this.latitude = response.data.results[0].geometry.location.lat;
        const calculated_response = await axios.post(
          "http://localhost:5001/calculator",
          {
            longitude: this.longitude,
            latitude: this.latitude,
            bedrooms: this.bedrooms,
            bathrooms: this.bathrooms,
            accommodates: this.accomodates,
            room_type: this.room_type,
            property_type: this.property_type,
            amenities: this.amenities,
            minimum_nights: this.minimum_nights,
            maximum_nights: this.maximum_nights,
          }
        );
        this.calculated_price = `€ ${calculated_response.data}`;
      } catch (error) {
        console.error(error);
      } finally {
        this.isLoading = false;
      }
    },
  },
};
</script>

<style>
#calculation.formkit-input {
  display: inline-flex !important;
}
button {
  color: rgb(0, 0, 0);
  background-color: rgb(178, 238, 150);
  text-align: center;
  text-decoration: none;
  font-size: 18px;
  cursor: pointer;
  margin-bottom: 16px !important;
  padding: 9px 13px;
  vertical-align: middle;
  overflow: hidden;
  border-radius: 40px;
  margin-left: 280px;
}
h1 {
  font-family: var(--fk-font-family-label);
  margin-left: 150px;
}

.input-container {
  display: flex;
  flex-wrap: wrap;
}

#image_home {
  padding-top: 25px !important;
  margin-right: 750px !important;
  margin-left: 1210px !important;
  border-radius: 60px !important;
  margin-top: -400px !important;
  min-width: 0 !important;
  padding-left: 100px !important;
}
.jumbotron {
  padding-top: 25px;
  margin-right: 750px;
  margin-left: 120px;
  border-radius: 60px;
  margin-top: 100px;
  min-width: 0;
  padding-left: 100px;
}

#calculated-price {
    width: 120px !important;
    height: 50px !important;
    margin-bottom: 50px;
}

.element3 {
  padding-top: 45px;
  margin-right: 550px;
  margin-left: 550px;
  border-radius: 60px;
  margin-top: 400px;
  min-width: 0;
  padding-left: 100px;
  border-top: 2px;
  border-top-style: solid;
  border-bottom: 2px;
  border-bottom-style: solid;
  border-left: 2px;
  border-left-style: solid;
  border-right: 2px;
  border-right-style: solid;
}
.btn {
  color: rgb(0, 0, 0);
  background-color: #dae6ff;
  text-align: center;
  text-decoration: none;
  font-size: 18px;
  cursor: pointer;
  margin-bottom: 16px !important;
  padding: 9px 13px;
  vertical-align: middle;
  overflow: hidden;
  border-radius: 40px;
  margin-top: 20px;
  margin-left: -5px;
  border-color: #92b3f8;
  --bs-btn-hover-border-color: #f95551;
}
.btn:hover {
  color: var(--bs-btn-hover-color);
  background-color: #f95551;
  border-color: var(--bs-btn-hover-border-color);
}
:root {
  --fk-color-primary: rgb(178, 238, 150) !important;
  --fk-color-button: rgb(0, 0, 0) !important;
  --fk-bg-submit-hover: rgb(99, 175, 64) !important;
  border-radius: 40px;
}

#second {
    width: 100%;
}

</style>
