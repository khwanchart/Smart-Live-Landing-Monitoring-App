def render_aircraft_card(selected_reg, ac_type, updated_date, wheels):
    nose_lh = wheel_html("LH", wheels["nose"].get("LH"), size="small")
    nose_rh = wheel_html("RH", wheels["nose"].get("RH"), size="small")

    main_1 = wheel_html("1", wheels["main"].get("1"), size="large")
    main_2 = wheel_html("2", wheels["main"].get("2"), size="large")
    main_3 = wheel_html("3", wheels["main"].get("3"), size="large")
    main_4 = wheel_html("4", wheels["main"].get("4"), size="large")

    card_html = f"""
<!DOCTYPE html>
<html>
<head>
<style>
    html, body {{
        margin: 0;
        padding: 0;
        background: transparent;
        font-family: Arial, Helvetica, sans-serif;
    }}

    .page-wrapper {{
        display: flex;
        justify-content: center;
        align-items: flex-start;
        width: 100%;
        padding-top: 10px;
        box-sizing: border-box;
    }}

    .aircraft-card {{
        width: 440px;
        min-height: 590px;
        border: 4px solid #000000;
        border-radius: 52px;
        background: #ffffff;
        overflow: hidden;
        color: #000000;
        box-sizing: border-box;
    }}

    .updated-date {{
        text-align: center;
        font-size: 28px;
        font-weight: 400;
        padding-top: 38px;
        padding-bottom: 8px;
        line-height: 1.2;
    }}

    .gold-strip {{
        background: #ead27a;
        text-align: center;
        font-size: 34px;
        font-weight: 400;
        line-height: 1.25;
        padding: 0 12px;
        box-sizing: border-box;
        width: 100%;
    }}

    .gold-strip.second {{
        margin-top: 5px;
    }}

    .nose-section {{
        margin-top: 14px;
        display: flex;
        justify-content: center;
    }}

    .main-section {{
        margin-top: 36px;
        display: flex;
        justify-content: center;
        gap: 38px;
    }}

    .wheel-pair {{
        position: relative;
        display: flex;
        justify-content: center;
        align-items: flex-start;
        box-sizing: border-box;
    }}

    /*
       Keep pair gap at zero because each wheel block already has enough width.
       This gives more room for text and avoids overlap.
    */
    .wheel-pair.nose-pair {{
        gap: 0;
    }}

    .wheel-pair.main-pair {{
        gap: 0;
    }}

    /*
       Black connector between tire blocks.
       It is centered vertically with the tire box, not with the whole text area.
    */
    .connector {{
        position: absolute;
        background: #000000;
        z-index: 1;
        border-radius: 2px;
        pointer-events: none;
        left: 50%;
        transform: translateX(-50%);
    }}

    /*
       Calculation:
       percent area is 24px high.
       Nose tire box is 46px high.
       Connector height is 10px.
       Top = 24 + 46 / 2 - 10 / 2 = 42px
    */
    .connector.nose-connector {{
        width: 54px;
        height: 10px;
        top: 42px;
    }}

    /*
       Calculation:
       percent area is 24px high.
       Main tire box is 64px high.
       Connector height is 10px.
       Top = 24 + 64 / 2 - 10 / 2 = 51px
    */
    .connector.main-connector {{
        width: 58px;
        height: 10px;
        top: 51px;
    }}

    .wheel-block {{
        position: relative;
        z-index: 2;
        display: flex;
        flex-direction: column;
        align-items: center;
        text-align: center;
        box-sizing: border-box;
    }}

    /*
       Important:
       These widths are intentionally wider than the tire box.
       This gives values like 100/290 and 440/450 their own space.
    */
    .wheel-block.small {{
        width: 96px;
    }}

    .wheel-block.large {{
        width: 92px;
    }}

    .percent-text {{
        font-size: 19px;
        line-height: 1.15;
        min-height: 24px;
        color: #ff6426;
        font-weight: 400;
        width: 100%;
        text-align: center;
        white-space: nowrap;
        overflow: hidden;
        box-sizing: border-box;
    }}

    .percent-placeholder {{
        min-height: 24px;
        line-height: 1.15;
        font-size: 19px;
        width: 100%;
        box-sizing: border-box;
    }}

    .wheel-box {{
        display: flex;
        justify-content: center;
        align-items: center;
        border: 2px solid #00304b;
        box-sizing: border-box;
        font-weight: 400;
        color: #ffffff;
        position: relative;
        z-index: 3;
    }}

    .wheel-block.small .wheel-box {{
        width: 56px;
        height: 46px;
        border-radius: 8px;
        font-size: 19px;
    }}

    .wheel-block.large .wheel-box {{
        width: 56px;
        height: 64px;
        border-radius: 9px;
        font-size: 29px;
    }}

    .wheel-box.warning {{
        background: #ffc20a;
        color: #ffffff;
    }}

    .wheel-box.danger {{
        background: #f34b3f;
        color: #ffffff;
    }}

    .wheel-box.normal {{
        background: #9fa8ad;
        color: #ffffff;
    }}

    .wheel-box.empty {{
        background: #9fa8ad;
        color: #ffffff;
    }}

    /*
       Text overlap fix:
       Each landing value is constrained to the full width of its wheel block.
       Font size is reduced slightly and centered.
    */
    .landing-value {{
        min-height: 28px;
        margin-top: 9px;
        font-size: 19px;
        line-height: 1.15;
        color: #ff6426;
        font-weight: 400;
        white-space: nowrap;
        width: 100%;
        text-align: center;
        overflow: hidden;
        box-sizing: border-box;
    }}

    .landing-value.empty {{
        color: transparent;
    }}

    .percent-text.empty {{
        color: transparent;
    }}

    .card-bottom-space {{
        height: 105px;
    }}
</style>
</head>

<body>
    <div class="page-wrapper">
        <div class="aircraft-card">
            <div class="updated-date">Update: {safe_text(updated_date)}</div>

            <div class="gold-strip">{safe_text(selected_reg)}</div>
            <div class="gold-strip second">{safe_text(ac_type)}</div>

            <div class="nose-section">
                <div class="wheel-pair nose-pair">
                    <div class="connector nose-connector"></div>
                    {nose_lh}
                    {nose_rh}
                </div>
            </div>

            <div class="main-section">
                <div class="wheel-pair main-pair">
                    <div class="connector main-connector"></div>
                    {main_1}
                    {main_2}
                </div>

                <div class="wheel-pair main-pair">
                    <div class="connector main-connector"></div>
                    {main_3}
                    {main_4}
                </div>
            </div>

            <div class="card-bottom-space"></div>
        </div>
    </div>
</body>
</html>
"""

    card_html = textwrap.dedent(card_html)

    components.html(
        card_html,
        height=670,
        scrolling=False
    )
