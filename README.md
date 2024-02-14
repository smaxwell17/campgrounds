# campgrounds
API for callers to retrieve campgrounds in a given state (stateCode) that cost less than a specified amount(costCap). The returned campground(s) must exist an a park that offers the activities specified by the caller (comma delimitated list)

Exists inside of a lambda and is executed via API gateway. 

The campground data is retrieved using the open source NPS apis.