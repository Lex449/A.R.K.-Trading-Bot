async def analyze_symbol(symbol: str, chat_id: int = None) -> dict | None:
    try:
        df = await fetch_market_data(symbol, chat_id=chat_id)
        if df is None or not validate_market_data(df):
            logger.warning(f"🚫 [AnalysisEngine] Data validation failed or no data returned for {symbol}.")
            if df is not None:
                logger.debug(f"⚠️ [Debug] {symbol} → Raw Close Prices (last 10): {df['c'].tail(10).tolist()}")
            if chat_id:
                from bot import application  # Lazy import to avoid circular import
                await application.bot.send_message(
                    chat_id=chat_id,
                    text=(
                        f"⚠️ *{symbol} konnte nicht analysiert werden:*\n"
                        f"_Grund:_ Kursdaten nicht valide oder leer.\n\n"
                        f"_Hinweis:_ API ist aktiv – das Symbol wurde bewusst übersprungen."
                    ),
                    parse_mode="Markdown"
                )
            return None

        last_price = df["c"].iloc[-1]

        # === Analyse-Module ===
        patterns = detect_patterns(df) or []
        volume_info = detect_volume_spike(df) or {}
        trend_info = detect_adaptive_trend(df) or {}
        indicator_score, trend_direction = evaluate_indicators(df) or (0.0, "Neutral")
        combined_action = determine_action(patterns, trend_info, indicator_score)

        risk_reward_info = (
            analyze_risk_reward(df, combined_action)
            if combined_action in ("Long 📈", "Short 📉")
            else None
        )

        base_confidence = calculate_confidence(patterns)
        adjusted_confidence = optimize_confidence(base_confidence, trend_info)

        if combined_action in ["Long 📈", "Short 📉"]:
            adjusted_confidence += 10
        adjusted_confidence = min(adjusted_confidence, 100.0)

        if adjusted_confidence < 50:
            signal_score = rate_signal(patterns, volatility_info=volume_info, trend_info=trend_info)
            if chat_id:
                from bot import application
                await application.bot.send_message(
                    chat_id=chat_id,
                    text=(
                        f"⛔ *{symbol} gefiltert – Confidence zu niedrig*\n\n"
                        f"*Confidence:* `{adjusted_confidence:.1f}%`\n"
                        f"*Patterns:* `{len(patterns)}`\n"
                        f"*Signal Score:* `{signal_score}/100`\n"
                        f"*Indicator Score:* `{indicator_score:.1f}`\n"
                        f"*Trend:* {trend_direction}\n\n"
                        f"_API war aktiv. Analyse lief erfolgreich – aber wurde bewusst gefiltert._"
                    ),
                    parse_mode="Markdown"
                )
            logger.info(
                f"⛔ [AnalysisEngine] {symbol} skipped – "
                f"Confidence: {adjusted_confidence:.1f}%, Patterns: {len(patterns)}, "
                f"Score: {signal_score}, IndicatorScore: {indicator_score}, Trend: {trend_direction}"
            )
            return None

        signal_category = categorize_signal(adjusted_confidence)
        signal_score = rate_signal(patterns, volatility_info=volume_info, trend_info=trend_info)

        result = {
            "symbol": symbol,
            "last_price": round(last_price, 2),
            "patterns": patterns,
            "avg_confidence": adjusted_confidence,
            "combined_action": combined_action,
            "signal_category": signal_category,
            "signal_score": signal_score,
            "indicator_score": indicator_score,
            "trend_direction": trend_direction,
            "volume_info": volume_info,
            "trend_info": trend_info,
            "risk_reward_info": risk_reward_info,
            "df": df
        }

        logger.info(
            f"✅ [AnalysisEngine] {symbol} | Action: {combined_action} | "
            f"Price: {last_price:.2f} | Confidence: {adjusted_confidence:.1f}% | Score: {signal_score}/100"
        )
        return result

    except Exception as e:
        logger.exception(f"❌ [AnalysisEngine] Critical failure for {symbol}: {e}")
        return None
