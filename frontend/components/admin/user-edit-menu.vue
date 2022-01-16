<template>
  <div>
    <v-menu
      bottom
      left
     >
      <template v-slot:activator="{ on, attrs }">
        <v-btn
          icon
          v-bind="attrs"
          v-on="on"
        >
          <v-icon>mdi-dots-vertical</v-icon>
        </v-btn>
      </template>

      <v-list>
        <v-list-item
          v-for="(item, index) in menu_items"
          :key="index"
          @click="handleClick(index)"
        >
          <v-list-item-icon>
            <v-icon v-text="item.icon"></v-icon>
          </v-list-item-icon>
          <v-list-item-content>
              <v-list-item-title v-text="item.title"></v-list-item-title>
          </v-list-item-content>
        </v-list-item>
      </v-list>
    </v-menu>

    <v-dialog v-model="show_edit_dialog" max-width="500px">
      <v-card>
        <v-card-title>Assign Role</v-card-title>
        <v-card-text>
          <v-container fluid>
            <v-radio-group v-model="userRole" style="width: 25%;">
              <v-radio
                label="Guest"
                value="guest"
              ></v-radio>
              <v-radio
                label="Member"
                value="member"
              ></v-radio>
            </v-radio-group>
          </v-container>
        </v-card-text>

        <v-card-actions>
          <v-spacer />
          <v-btn class="blue--text darken-1" text @click="show_edit_dialog = false">Cancel</v-btn>
          <v-btn class="blue--text darken-1" text @click="updateUser()" >Save</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
export default {
		props: ['user'],
    data: () => ({
      userRole: 'guest',
      show_edit_dialog: false,
      menu_items: [
        { 
          title: 'Edit',
          icon: 'mdi-pencil',
          async click(){
            this.show_edit_dialog = true
          }
        },
        { 
          title: 'Delete',
          icon: 'mdi-delete',
          async click(){
            let data = await this.$store.dispatch(
              'auth/deleteUserByAdmin', 
              {username: this.user.username, company_code: this.user.company_code}
            )
						if (data === "ok"){
							this.$emit('user-deleted')
						}
          }
        },
      ]
    }),
    methods: {
      handleClick(index){
        //this.menu_items[id].click()  #will get erros, because of function click will no can access propertie with it's own 'this'
        this.menu_items[index].click.call(this) // will call the function but the function will use the vue instance 'this' context.
      },
      updateUser(){
        this.$store.dispatch("auth/updateUser", {username: this.user.username, role: this.userRole})
        console.log(">>>>>>> ", this.user.roles)
        this.user.role = this.userRole
      }
  },

  /** created(){ */
      /** let data = await this.$store.dispatch("auth/fetchRoles", { */
        /** verbose_name: this.verbose_name,  */
        /** table_code: this.table_code, */
        /** description: this.description, */
        /** price_items: this.price_items */
      /** }) */
      /** if (data) { */
        /** this.pricetables.push(data); */
      /** } */
  /** } */
}
</script>
