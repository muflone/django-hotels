jQuery(document).ready(function($) {
    console.log('Customizing DateTime widget');
    DateTimeShortcuts.clockHours.default_ = [];
    for (let hour = 6; hour <= 21; hour++) {
        let verbose_name = new Date(1970, 1, 1, hour, 0, 0).strftime('%H:%M');
        DateTimeShortcuts.clockHours.default_.push([verbose_name, hour])
    }
});
